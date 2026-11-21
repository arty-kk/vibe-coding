'use strict';
(() => {
  const fold = value => String(value ?? '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
  const words = value => fold(value).match(/[\p{L}\p{N}+#]+/gu) || [];
  const compact = value => fold(value).replace(/[^\p{L}\p{N}+#]/gu, '');
  const escape = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const cjk = value => /[\u3400-\u9fff]/u.test(value);
  const contains = (haystack, term) => cjk(term)
    ? haystack.some(word => word.includes(term))
    : haystack.some(word => word === term || (term.length >= 3 && word.startsWith(term)));
  const compiled = new WeakMap(), bodyCache = new WeakMap();

  function oneEdit(a, b) {
    if (Math.abs(a.length - b.length) > 1) return false;
    if (a === b) return true;
    let i = 0;
    while (i < Math.min(a.length, b.length) && a[i] === b[i]) i++;
    if (a.length === b.length) return a.slice(i + 1) === b.slice(i + 1)
      || i + 1 < a.length && a[i] === b[i + 1] && a[i + 1] === b[i]
        && a.slice(i + 2) === b.slice(i + 2);
    return a.length > b.length ? a.slice(i + 1) === b.slice(i) : a.slice(i) === b.slice(i + 1);
  }

  function typoCorrector(rules, entries) {
    const forms = new Set(Object.values(rules.lexicon.terms || {}).flat()
      .concat(Object.keys(rules.lexicon.terms || {}), Object.values(rules.lexicon.intents || {}).flat()));
    for (const entry of entries) {
      for (const text of [entry.id, entry.skill, ...entry.titles, ...(entry.keywords || [])]) {
        for (const word of words(text)) forms.add(word);
      }
    }
    const exact = new Set([...forms].flatMap(words).concat([...rules.stops]));
    const deletions = new Map(), signature = word => rules.signature(word);
    for (const word of exact) {
      if (rules.stops.has(word) || word.length < 5 || word.length > 48 || cjk(word) || !/^\p{L}+$/u.test(word)) continue;
      for (let i = 0; i < word.length; i++) {
        const key = word.slice(0, i) + word.slice(i + 1);
        if (!deletions.has(key)) deletions.set(key, new Set());
        deletions.get(key).add(word);
      }
    }
    return value => fold(value).replace(/[\p{L}\p{N}+#]+/gu, word => {
      if (exact.has(word) || word.length < 5 || word.length > 48 || cjk(word) || !/^\p{L}+$/u.test(word)) return word;
      const candidates = new Set(deletions.get(word) || []);
      for (let i = 0; i < word.length; i++) {
        const key = word.slice(0, i) + word.slice(i + 1);
        if (exact.has(key) && !rules.stops.has(key)) candidates.add(key);
        for (const item of deletions.get(key) || []) candidates.add(item);
      }
      const matches = [...candidates].filter(item => item.length >= 5 && item[0] === word[0] && oneEdit(word, item));
      if (!matches.length || new Set(matches.map(signature)).size !== 1) return word;
      return matches.sort()[0];
    });
  }

  function replacer(groups) {
    const table = new Map();
    for (const [target, variants] of Object.entries(groups || {})) {
      for (const value of [target, ...variants]) table.set(fold(value), target);
    }
    const variants = [...table.keys()].sort((a, b) => b.length - a.length || a.localeCompare(b));
    if (!variants.length) return value => value;
    const pattern = new RegExp(variants.map(value => cjk(value) ? escape(value)
      : '(?<![\\p{L}\\p{N}])' + escape(value) + '(?![\\p{L}\\p{N}])').join('|'), 'gu');
    return value => value.replace(pattern, match => ' ' + table.get(match) + ' ');
  }

  function taskGoal(text, groups) {
    if (!groups?.length) return null;
    const normalized = ' ' + words(text).join(' ') + ' ';
    const mentions = phrase => cjk(phrase) ? normalized.includes(fold(phrase))
      : normalized.includes(' ' + words(phrase).join(' ') + ' ');
    for (const group of groups) {
      if (!group.subjects.some(mentions)) continue;
      const goal = group.goals.find(route => route.phrases.some(mentions));
      if (goal) return goal;
    }
    return null;
  }

  function rulesFor(lexicon) {
    if (!compiled.has(lexicon)) {
      const concepts = replacer(lexicon.terms);
      const intents = replacer(Object.fromEntries(Object.entries(lexicon.intents || {}).map(([mode, values]) => ['intent_' + mode, values])));
      const stops = new Set((lexicon.stopwords || []).map(fold));
      // CJK filler removal is exact phrase replacement, not an unrestricted stemmer.
      const cleanCjk = text => {
        for (const stop of [...stops].filter(cjk).sort((a, b) => b.length - a.length)) text = text.replaceAll(stop, ' ');
        return text;
      };
      compiled.set(lexicon, {lexicon, stops,
        signature: value => intents(concepts(fold(value))).trim(),
        tokens: value => words(concepts(fold(value))),
        query: (value, correct) => {
          const text = intents(concepts(correct ? correct(value) : fold(value)));
          const hints = [...text.matchAll(/intent_([a-z]+)/g)].map(match => match[1]);
          const terms = words(cleanCjk(text.replace(/intent_[a-z]+/g, ' '))).filter(term => !stops.has(term));
          return {terms: [...new Set(terms)], hints: [...new Set(hints)], goal: taskGoal(value, lexicon.goal_routes)};
        }});
    }
    return compiled.get(lexicon);
  }

  function prepare(entries, topics, actions, lexicon = {}) {
    const base = rulesFor(lexicon);
    const correct = typoCorrector(base, entries);
    const rules = {...base, query: value => base.query(value, correct)};
    return entries.map((entry, order) => ({...entry, order, rules,
      titleWords: rules.tokens(entry.titles.join(' ')),
      subjects: (entry.primary_keywords || []).map(value => rules.tokens(value)),
      keywordWords: rules.tokens([entry.id, entry.skill, entry.purpose || '', ...(entry.keywords || []),
        ...(lexicon.discovery?.[entry.id] || [])].join(' ')),
      topicWords: rules.tokens((topics[entry.skill] || []).join(' ')),
      actionWords: rules.tokens([entry.mode, ...(actions[entry.mode] || [])].join(' ')),
      exactId: compact(entry.id),
      exactTitles: entry.titles.map(compact),
      exactAliases: (lexicon.aliases?.[entry.id] || []).map(compact)
    }));
  }

  function bodyWords(entry, bodies) {
    if (!bodyCache.has(bodies)) bodyCache.set(bodies, new Map());
    const cache = bodyCache.get(bodies);
    if (!cache.has(entry.id)) cache.set(entry.id, entry.rules.tokens(bodies[entry.id]?.body || ''));
    return cache.get(entry.id);
  }

  function score(entry, query, analysis, bodies) {
    const key = analysis.key;
    const exact = key && (key === entry.exactId ? 'exact_id'
      : entry.exactTitles.includes(key) ? 'exact_title' : entry.exactAliases.includes(key) ? 'alias' : null);
    if (exact) return {score: exact === 'exact_id' ? 20000 : 15000, bodyOnly: false, kind: exact, terms: analysis.terms};
    const isGoal = entry.id === analysis.goal?.id;
    if (isGoal && analysis.goal.prefer) return {score: 8000, bodyOnly: false, kind: 'catalog', terms: []};
    let total = 0, bodyOnly = false;
    for (const term of analysis.terms) {
      if (entry.subjects.some(subject => contains(subject, term)
        && subject.every(part => analysis.terms.some(queryTerm => contains([part], queryTerm))))) total += 60;
      else if (contains(entry.titleWords, term)) total += 40;
      else if (contains(entry.keywordWords, term)) total += 20;
      else if (contains(entry.topicWords, term)) total += 8;
      else if (bodies && contains(bodyWords(entry, bodies), term)) {total += 1; bodyOnly = true;}
      else return isGoal ? {score: -2000, bodyOnly: false, kind: 'catalog', terms: []} : null;
    }
    if (analysis.hints.includes(entry.mode)) total += 35;
    if (bodyOnly) total -= 1000;
    return {score: total, bodyOnly, kind: bodyOnly ? 'instruction_body' : query.trim() ? 'catalog' : 'browse', terms: analysis.terms};
  }

  function select(entries, state, bodies) {
    const query = state.q || '';
    const analysis = entries[0]?.rules.query(query) || {terms: words(query), hints: []};
    analysis.key = compact(query);
    const collect = parsed => entries.map(entry => ({entry, match: score(entry, query, parsed, state.full ? bodies : null)}))
      .filter(item => item.match !== null);
    let candidates = collect(analysis);
    if (!candidates.length && !state.full && analysis.terms.length > 2) {
      // Retry only after an empty result. Keep every term known to the catalog,
      // and require at least two terms representing at least half of the request.
      const terms = analysis.terms.filter(term => entries.some(entry =>
        contains(entry.titleWords, term) || contains(entry.keywordWords, term) || contains(entry.topicWords, term)));
      if (terms.length >= 2 && terms.length < analysis.terms.length && terms.length * 2 >= analysis.terms.length) {
        candidates = collect({...analysis, terms, key: ''});
      }
    }
    const topics = {}, actions = {};
    for (const {entry} of candidates) {
      if (!state.action || entry.mode === state.action) topics[entry.skill] = (topics[entry.skill] || 0) + 1;
      if (!state.topic || entry.skill === state.topic) actions[entry.mode] = (actions[entry.mode] || 0) + 1;
    }
    const matches = candidates.filter(({entry}) => (!state.topic || entry.skill === state.topic) && (!state.action || entry.mode === state.action))
      .sort((a, b) => b.match.score - a.match.score || (query.trim()
        ? Number(a.entry.mode !== 'audit') - Number(b.entry.mode !== 'audit') || a.entry.id.localeCompare(b.entry.id)
        : a.entry.order - b.entry.order));
    return {matches, topics, actions};
  }

  function readState(search, topics, actions) {
    const params = new URLSearchParams(search);
    const topic = params.get('topic') || params.get('category') || '';
    const action = params.get('action') || params.get('mode') || '';
    const page = Number(params.get('page'));
    return {q: (params.get('q') || '').slice(0, 240),
      topic: topics.includes(topic) ? topic : '', action: actions.includes(action) ? action : '',
      full: params.get('full') === '1', page: Number.isSafeInteger(page) && page > 0 ? page : 1};
  }

  function searchParams(state) {
    const params = new URLSearchParams();
    if (state.q.trim()) params.set('q', state.q.trim());
    if (state.topic) params.set('topic', state.topic);
    if (state.action) params.set('action', state.action);
    if (state.full) params.set('full', '1');
    if (state.page > 1) params.set('page', String(state.page));
    return params.toString();
  }

  function paginate(matches, requested, size = 12) {
    const pages = Math.max(1, Math.ceil(matches.length / size));
    const page = Math.min(Math.max(1, requested), pages);
    const start = (page - 1) * size;
    return {items: matches.slice(start, start + size), page, pages, total: matches.length,
      from: matches.length ? start + 1 : 0, to: Math.min(start + size, matches.length)};
  }

  function safeReturn(value, origin, base) {
    if (!value || value.length > 2400) return null;
    try {
      const url = new URL(value, origin);
      const routes = ['', 'es/', 'ru/', 'zh-CN/'].map(route => base + route);
      return url.origin === origin && routes.includes(url.pathname) ? url.pathname + url.search + '#catalog' : null;
    } catch {return null;}
  }

  const engine = {fold, words, prepare, select, readState, searchParams, paginate, safeReturn};
  if (typeof module !== 'undefined' && module.exports) module.exports = engine;
  else window.VibeCatalog = engine;
})();

window.VibeCatalog.lexicon = {"version":1,"terms":{"cache":["caching","caches","cached","кэш","кеш","кэша","кеша","кэшем","кешем","кэширование","кеширование","caché","almacenamiento en cache","缓存"],"api":["apis","interface api","апи","интерфейс api","接口"],"authentication":["auth","authenticate","login","sign in","аутентификация","аутентификации","вход","авторизация входа","autenticación","inicio de sesión","身份验证","登录","аутентификацию","войти","входа","не могу войти","не удается войти","не получается войти","не пускает в аккаунт","sign-in","signin","log in","cannot log in","no puedo iniciar sesión","no puedo entrar","无法登录","логин","логина","вход в аккаунт","вход в систему"],"authorization":["permissions","permission","access control","доступ","доступа","прав доступа","разрешения","разрешений","autorización","permisos","权限","授权","авторизация","авторизации","авторизацию","авторизацией","авторизационные","право доступа","права доступа","права","правами","допуск","access rights","authorisation","прав","полномочия","полномочий","доступом","доступу","нет доступа","отказано в доступе","доступ запрещен","access denied","permission denied","forbidden","403","sin acceso","acceso denegado","权限不足","没有权限"],"tenant":["tenants","tenancy","мультитенантность","тенант","тенанта","арендатора","inquilino","multiinquilino","租户","多租户","тенантов","тенантами","inquilinos"],"payment":["payments","charge","charges","платеж","платежи","платежей","оплата","списание","списания","pagos","pago","cobro","cobros","支付","扣款"],"webhook":["webhooks","вебхук","вебхуки","вебхуков","网络钩子","вебхука"],"retry":["retries","retried","повторная попытка","повторные попытки","повторных попыток","ретраи","ретраях","reintentos","reintento","重试"],"duplicate":["duplicates","duplicated","repeated","дубли","дубликаты","дублирование","дублируется","повторные","duplicado","duplicados","duplicadas","重复"],"queue":["queues","очередь","очереди","очередей","очередью","cola","colas","队列"],"delivery":["delivered","доставка","доставки","entrega","entregas","投递","交付"],"shutdown":["shut down","остановка","остановки","завершение работы","apagado","cierre del worker","关闭","остановку"],"worker":["workers","воркер","воркера","воркеров","trabajador","trabajadores","工作进程"],"rollback":["roll back","откат","отката","откатить","reversión","revertir","回滚"],"recovery":["recover","restore","restoration","восстановление","восстановления","восстановить","recuperación","restauración","恢复"],"freshness":["stale","staleness","устаревшие","устаревший","устаревшие данные","актуальность","frescura","obsoletos","obsoletas","新鲜度","过期"],"search":["searching","поиск","поиска","поиске","поисковый","búsqueda","buscar","搜索","检索"],"vector":["vectors","embedding","embeddings","вектор","векторы","векторной","эмбеддинги","vectorial","vectores","向量","嵌入"],"index":["indexes","indexing","индекс","индекса","индексация","índice","índices","indexación","索引"],"localization":["localisation","i18n","l10n","translation","translations","локализация","локализации","локализацию","переводы","переводов","localización","traducción","traducciones","本地化","翻译"],"accessibility":["a11y","доступность интерфейса","доступность","accesibilidad","无障碍","可访问性"],"hydration":["hydrate","hydrating","гидратация","гидратации","гидратацию","hidratación","水合"],"web":["website","websites","веб","сайта","sitio web","网站","сайт","сайты","сайтик","сайтики","sitio","web page","网页"],"notification":["notifications","уведомление","уведомления","уведомлений","notificación","notificaciones","通知"],"observability":["наблюдаемость","наблюдаемости","observabilidad","可观测性"],"logs":["logging","log","логи","логов","журналирование","registros","日志"],"metrics":["metric","метрики","метрик","метрика","métrica","métricas","指标"],"performance":["производительность","производительности","rendimiento","性能"],"latency":["задержка","задержки","latencia","延迟"],"concurrency":["concurrent","конкурентность","конкурентных","параллельные","concurrencia","concurrentes","并发"],"idempotency":["idempotent","идемпотентность","идемпотентности","idempotencia","幂等"],"consistency":["consistent","консистентность","согласованность","согласованности","consistencia","一致性"],"migration":["migrations","миграция","миграции","migración","migraciones","迁移"],"backup":["backups","резервная копия","резервные копии","бэкапы","copia de seguridad","copias de seguridad","备份"],"privacy":["приватность","персональные данные","конфиденциальность","privacidad","隐私"],"security":["безопасность","безопасности","seguridad","安全"],"workflow":["workflows","воркфлоу","flujo de trabajo","flujos de trabajo","工作流"],"plan":["planning","план","планирование","планирования","planificación","规划"],"replay":["воспроизведение истории","реплей","reproducción de historial","历史重放","重放"],"serverless":["server less","sin servidor","серверлесс","бессерверный","бессерверных","无服务器"],"object storage":["s3","object stores","объектное хранилище","объектного хранилища","almacenamiento de objetos","对象存储"],"sql":["postgres","postgresql","mysql","реляционная база","реляционной базы","关系数据库"],"nosql":["mongodb","dynamodb","cassandra","нереляционная база","非关系数据库"],"kubernetes":["k8s","кубернетес","кубернетеса"],"kafka":["redpanda","кафка","кафки"],"rabbitmq":["rabbit mq","рэббит"],"celery":["селери"],"redis":["bullmq","редис","редиса"],"clickhouse":["click house","кликхаус"],"mcp":["model context protocol","мсп"],"ai":["artificial intelligence","искусственный интеллект","inteligencia artificial","人工智能"],"rag":["retrieval augmented generation","rag pipeline","检索增强生成"],"ocr":["document ai","распознавание документов","reconocimiento de documentos","文档识别"],"mobile":["мобильное приложение","мобильных приложений","aplicación móvil","移动应用"],"desktop":["десктоп","настольное приложение","aplicación de escritorio","桌面应用"],"extension":["browser extension","расширение браузера","extensión del navegador","浏览器扩展"],"feature flag":["feature flags","фича флаг","фичефлаги","bandera de función","功能开关"],"form":["forms","форма","формы","formulario","formularios","表单"],"onboarding":["онбординг","incorporación","用户引导"],"experiment":["experiments","эксперимент","эксперимента","experimento","实验"],"analytics":["аналитика","аналитики","analítica","分析"],"billing":["entitlements","биллинг","биллинга","facturación","计费"],"contract":["contracts","контракт","контракта","контрактов","contrato","contratos","契约"],"invariant":["invariants","инвариант","инварианта","invariante","invariantes","不变量"],"patch":["патч","патча","parche","补丁"],"release":["releases","релиз","релиза","lanzamiento","发布"],"framework":["фреймворк","фреймворка","框架"],"query":["queries","запрос","запросы","consulta","consultas","查询"],"failure":["failures","failed","ошибка","ошибки","сбой","сбоя","fallo","fallos","故障"],"deploy":["deployment","развертывание","деплой","despliegue","部署"],"database":["databases","база данных","базы данных","базе данных","base de datos","bases de datos","数据库"],"isolation":["изолировать","изоляция","изоляции","изоляцию","aislamiento","aislar","隔离"],"consumer":["consumers","консьюмер","консьюмера","консьюмеров","потребитель","потребителя","consumidor","consumidores","消费者"],"rebalance":["rebalancing","ребалансировка","ребалансировки","ребалансировку","rebalanceo","reequilibrio","重平衡"],"ssr":["server side rendering","server rendering","серверный рендеринг","серверного рендеринга","renderizado del servidor","服务端渲染","服务器渲染"],"write":["writes","запись","записи","записью","escritura","escrituras","写入"],"read":["reads","чтение","чтения","lectura","lecturas","读取"],"delete":["deletion","deleted","deletes","удаление","удаления","eliminar","eliminación","删除"],"crash":["crashes","crashed","падение","падения","caída","caídas","崩溃"],"state":["states","состояние","состояния","estado","estados","状态"],"session":["sessions","сессия","сессии","сессию","sesión","sesiones","会话","сессий","сессиями"],"upgrade":["upgrades","обновление","обновления","actualización","升级"],"upload":["uploads","загрузка файла","загрузки файла","carga de archivos","subida","上传"],"flag":["flags","флаг","флага","bandera","标志"],"tool":["tools","herramienta","herramientas","инструмент","инструментов","тул","тулов","工具"],"description":["descriptions","descripción","descripciones","описание","описания","描述"],"partition":["partitions","партиция","раздел","partición","分区"],"lock":["locks","locking","блокировка","bloqueo","锁"],"ingestion":["ingest","ingesting","ingesta","загрузка данных","摄取"],"oauth":["oauth2","oauth 2","oauth 2.0"],"oidc":["openid connect"],"role":["roles","роль","роли","ролей","rol","角色"],"policy":["policies","политика","политики","политик","política","políticas","策略"],"attribute":["attributes","атрибут","атрибуты","атрибутов","atributo","atributos","属性"],"user":["users","пользователь","пользователя","пользователи","пользователей","usuario","usuarios","用户"],"password":["passwords","пароль","пароли","паролей","contraseña","contraseñas","密码"],"token":["tokens","токен","токены","токенов","令牌"],"backend":["back end","бэкенд","бэкенда","бэкэнд","бэкэнда","серверная часть","后端"],"homepage":["home page","главная","главной","главную","главная сайта","главную сайта","главная страница","главной страницы","главную страницу","página de inicio","página principal","首页","主页"],"landing page":["landing","landingpage","лендинг","лендинга","лендингу","лендинги","лендингов","посадочная страница","посадочной страницы","посадочную страницу","página de aterrizaje","página de destino","落地页","着陆页"],"visual design":["beautiful","beautiful design","красивый","красивую","красивое","красивого","красиво","дизайн","дизайна","эстетика","эстетизм","эстетичный","diseño visual","diseño","视觉设计"],"art direction":["арт-дирекшн","артдирекшн","арт-дирекшен","художественное направление","dirección artística","艺术方向"],"modern":["современный","современная","современную","современное","современного","ultramodern","ультрасовременный","moderno","moderna","现代","现代化"],"premium":["премиальный","премиальная","премиальную","премиального","премиум","премиальности","sofisticado","高端"],"structure":["структура","структуру","структуры","estructura","结构"],"references":["reference","референс","референсы","референсов","референсами","примеры сайтов","referencias","参考","设计参考"],"design assets":["графические материалы","графика","графики","ресурсы дизайна","recursos gráficos","设计素材","图形素材"],"offer":["предложение","оффер","оффера","ценностное предложение","oferta","价值主张"],"conversion":["воронка","воронки","конверсия","конверсии","conversión","转化"],"page structure":["структура страницы","структура главной","страничная структура","estructura de página","页面结构"],"website brief":["задание на сайт","задание для сайта","пакет для реализации","техническое задание сайта","brief del sitio","网站实施方案"],"requirement coverage":["полнота требований","покрытие требований","ничего не пропустить","cobertura de requisitos","需求覆盖"],"copywriting":["копирайт","копирайтинг","тексты сайта","текст сайта","redacción web","文案","网站文案"],"microcopy":["микрокопирайт","микрокопирайтинг","микротексты","микротекст","тексты кнопок","текст кнопки","交互提示","微文案"],"grammar":["грамматика","грамматики","профессиональный текст","gramática","语法"],"declension":["склонение","склонения","согласование","词形"],"brand identity":["айдентика","бренд-комплект","брендбук","identidad de marca","品牌标识"],"logo":["логотип","логотипы","логотипа","логотипов","лого","logotipo","logotipos","标志"],"favicon":["фавикон","фавикона","фавиконы","фавиконов","фавиконка","网站图标"],"icon":["icons","иконка","иконки","иконок","иконку","iconos","图标"],"font":["fonts","шрифт","шрифты","шрифтов","шрифта","fuente","fuentes","字形"],"typography":["типографика","типографики","типографику","типографию","типография","tipografía","字体","排版"],"palette":["палитра","палитры","палитру","цвета","цветов","цветовую палитру","paleta","colores","配色","色板"],"grid":["сетка","сетку","сетки","retícula","网格"],"geometry":["геометрия","геометрии","геометрию","геометрией","геометричность","geometría","几何"],"layout":["верстка","вёрстка","вёрстки","верстки","раскладка","компоновка","maquetación","布局"],"components":["component","блоки","блоков","блока","компоненты","компонентов","компонент","componentes","组件","区块"],"visual hierarchy":["визуальная иерархия","визуальной иерархии","иерархия","акценты","акцентов","акценты страницы","jerarquía visual","视觉层级"],"height":["высота","высоты","высоту","altura","高度"],"hero":["hero section","хиро","первый экран","первого экрана","первом экране","primer bloque","首屏"],"header":["хедер","хедера","хедере","шапка","шапки","шапку","cabecera","页头"],"footer":["футер","футера","футере","подвал","подвала","pie de página","页脚"],"navigation":["навигация","навигации","навигацию","меню","navegación","导航"],"interaction states":["состояния кнопок","состояния элементов","состояния блоков","estados de interacción","交互状态"],"button":["buttons","кнопка","кнопки","кнопок","кнопку","botón","botones","按钮"],"motion":["animation","animations","transition","transitions","анимация","анимации","анимацию","анимацией","переходы","переходов","анимационные переходы","animación","transiciones","动画","过渡"],"interaction design":["интерактив","интерактива","интерактивность","сценарии взаимодействия","interacción","交互设计"],"gradient":["gradients","градиент","градиенты","градиента","градиентов","degradado","degradados","渐变"],"glass":["glassmorphism","стекло","стекла","стеклом","стеклянный","cristal","vidrio","玻璃"],"shadow":["shadows","тень","тени","теней","sombra","sombras","阴影"],"transparency":["opacity","прозрачность","прозрачности","прозрачные","альфа","transparencia","透明度"],"border":["borders","outline","обводки","обводка","обводок","бордеры","контуры элементов","bordes","边框"],"depth":["объём","объем","объёмные формы","объемные формы","объёмные","объемные","profundidad","立体"],"3d":["3D scene","3d graphics","3d сцена","трехмерная графика","трёхмерная графика","3d场景"],"procedural graphics":["algorithmic background","generative background","алгоритмический фон","алгоритмические фоны","алгоритмический","алгоритмическая","алгоритмические","процедурная графика","генеративная графика","шейдер","shader","fondos generativos","算法背景","程序化图形"],"design kit":["дизайн-пакет","дизайн пакет","набор материалов","kit de diseño","设计素材包"],"monorepo":["monorepository","монорепо","монореп","монорепозиторий","монорепозитория","монорепа","монорепы","monorepositorio","单体仓库"],"project architecture":["архитектура проекта","архитектура сайта","архитектура веб-проекта","arquitectura del proyecto","项目架构"],"stack":["tech stack","technology stack","стек","стека","стеком","pila tecnológica","技术栈"],"seo":["поисковая оптимизация","搜索引擎优化"],"geo":["generative engine optimization","генеративная оптимизация","生成式搜索优化"],"loading":["загрузка","загрузки","загрузку","скорость загрузки","carga","加载"],"calculator":["калькулятор","калькулятора","калькуляторы","calculadora","计算器"],"pricing":["тарифы","тарифов","тариф","цены","тарификация","precios","tarifas","定价"],"carousel":["slider","sliders","слайдер","слайдеры","слайдера","карусель","карусели","carrusel","轮播"],"lead magnet":["лидмагнит","лид-магнит","лидмагниты","лидмагнита","recurso descargable","引流资料"],"social proof":["соцдоказательства","социальные доказательства","отзывы","prueba social","社会证明"],"responsive":["адаптивность","адаптивный","адаптивная","адаптивности","адаптивную","responsive design","адаптив","adaptable","响应式"],"finish":["доделать","доделка","завершить сайт","завершение сайта","terminar","完善"],"redesign":["редизайн","редизайна","переделка","переделать","rediseño","重新设计"],"architecture":["архитектура","архитектуры","архитектуру","arquitectura","架构"]},"intents":{"audit":["audit","auditing","auditoría","auditar","аудит","проаудировать","检查缺陷","审计"],"implement":["implement","implementation","fix","repair","improve","polish","исправь","исправить","почини","починить","улучши","улучшить","реализуй","реализовать","исправление","implementación","implementar","arreglar","corrige","corregir","mejorar","mejora","reparar","修复","改进","实现","настроить","настройка","configure","configurar","配置","add","adding","добавить","добавь","внедрить","añadir","agregar","添加","build","create","make","создай","создать","сделай","сделать","сверстай","сверстать","доделай","доделать","переделай","переделать","redesign","finish","crear","construir","制作","创建","搭建"],"check":["check","verify","verification","validate","validation","проверь","проверить","проверка","проверки","верификация","verifica","verificar","comprobar","comprobación","validar","验证","检查"],"review":["review","ревью","revisión","评审"],"map":["map","mapping","карта","карту","картирование","mapa","地图"],"plan":["plan","planning","план","планирование","планировать","planificación","planificar","规划","shape","shaping"],"probe":["probe","find one bug","найди один баг","encontrar un error","查找一个错误","глючит","глючет","сломалось","сломался","не работает","broken","glitching","misbehaving","no funciona","出故障","glitch","glitches","debug","debugging","diagnose","diagnosis","глюк","глюки","отладка","отладить"],"document":["document","documentation","документация","документировать","documentar","documentación","文档","update the readme"],"closure":["closure","close iteration","закрытие итерации","cierre de iteración","迭代收尾"]},"stopwords":["a","about","after","agent","agents","al","already","an","and","are","as","at","ayuda","ayudar","be","been","before","being","biblioteca","by","can","code","coding","como","con","correct","correctly","could","cómo","de","del","des","do","does","during","el","en","engineering","existing","favor","find","flujo","flujos","for","from","get","getting","give","has","have","help","how","i","improve","in","into","is","issue","it","its","keeps","kept","la","las","library","los","me","mi","mis","my","necesito","need","nuestra","nuestro","o","of","on","or","our","para","please","por","porfavor","problem","properly","que","quiero","really","repeatedly","should","sin","task","that","the","these","this","those","to","trabajo","un","una","unas","unexpectedly","unos","update","use","used","using","want","was","we","well","what","when","where","which","while","why","with","workflow","workflows","would","y","your","агент","агента","библиотека","блин","в","во","где","для","до","еще","ещё","и","из","или","использовать","используй","к","кажется","как","какая","какие","какой","ко","когда","мне","моей","моем","мой","на","надо","найди","найти","нам","наш","непонятно","нормально","нужен","нужна","нужно","нужны","о","об","от","очень","перед","по","пожалуйста","помоги","после","постоянно","почему","правильно","при","проблема","проблемой","проверить","проект","проекте","работает","работать","с","скилл","скиллы","со","там","то","у","хочется","хочу","что","чтото","эта","эти","это","этот","代理","代码","使用","如何","工作流","工程","帮我","库","怎么","我的","请","请帮我","这个","问题","需要"],"aliases":{"patch-checking":["Patch Check","PatchCheck","PatchChecking","code review","review my patch","проверка патча","ревью патча","revisión del parche","补丁检查"],"task-shaping":["shape a task","task brief","постановка задачи","формулировка задачи","definir una tarea","任务定义"],"project-atlas-map":["repository map","repo map","карта проекта","mapa del proyecto","项目地图"],"homepage-landing-polish":["улучши главную","улучшить главную","доделай сайт","доделать сайт","переделай главную","переделать главную","доделай лендинг","redesign homepage","improve homepage","finish this website","finish website","finish homepage","rediseñar la página de inicio","完善首页"],"homepage-landing-build":["создай лендинг","сделай лендинг","build a landing page","create homepage","build homepage","создай сайт с нуля","сделай сайт с нуля"],"web-page-architecture":["структура главной","структура главной сайта","структура лендинга","homepage structure"],"web-visual-system":["типографика палитра","homepage typography"],"web-experience-brief":["задание на сайт","пакет для реализации сайта","полное задание на сайт"]},"discovery":{"payments-webhook-reconciliation-check":["duplicate payment webhook retry reconciliation","повторное списание","cobros duplicados","重复扣款"],"payments-provider-polish":["fix duplicate charge payment webhook","исправить повторное списание","corregir cobros duplicados"],"idempotency-concurrency-audit":["race condition double effect stale owner conflicting writes"],"idempotency-concurrency-polish":["fix race condition duplicate effects conflicting writes"],"web-rendering-audit":["SSR hydration mismatch saved theme locale timezone"],"web-rendering-polish":["fix hydration mismatch saved theme locale timezone","SSR hydration first server client render"],"web-boundary-check":["verify SSR hydration server action cache identity"],"cache-invalidation-polish":["fix stale cache invalidation old value after write"],"cache-coherency-check":["verify stale cache invalidation after write"],"search-index-audit":["missing search results wrong ranking relevant documents"],"search-index-polish":["fix search results ranking recall freshness"],"mcp-server-audit":["MCP tool discovery description schema model tool choice"],"mcp-server-polish":["improve MCP tool descriptions discovery model tool choice"],"llm-agent-tools-audit":["agent wrong tool choice tool selection ignores tools"],"llm-agent-tools-polish":["fix agent tool selection wrong arguments ignored tools"],"agent-harness-audit":["agent execution resume crash durable state replay"],"agent-harness-polish":["fix agent execution resume crash durable state"],"rag-audit":["retrieval sources citations unsupported answers"],"rag-polish":["fix retrieval sources citations unsupported answers"],"rbac-abac-matrix-check":["verify role permission policy allowed denied matrix"],"auth-permissions-audit":["login session token refresh logout authentication authorization"],"auth-permissions-polish":["fix login session token refresh logout"],"object-storage-integrity-recovery-check":["verify object upload checksum version restore"],"celery-delivery-shutdown-check":["verify Celery acknowledgement worker shutdown retry duplicate"],"kafka-redpanda-rebalance-failure-check":["verify Kafka consumer rebalance offset replay duplicate"],"rabbitmq-redelivery-recovery-check":["verify RabbitMQ acknowledgement connection loss redelivery"],"redis-queue-load-recovery-check":["verify Redis BullMQ stalled worker reclaim duplicate"],"feature-flag-exposure-rollback-check":["verify feature flag exposure kill switch rollback"],"mobile-release-offline-check":["verify mobile offline sync upgrade migration device"],"local-client-runtime-security-check":["verify desktop extension IPC sender permission update"],"product-landing-copy-polish":["rewrite landing page copy headline positioning"],"seo-geo-polish":["improve SEO GEO structured data canonical crawler indexing"],"performance-budget-audit":["latency memory CPU cost resource budget regression"],"release-artifact-trust-check":["verify SBOM provenance signature final artifact digest"],"iteration-closure":["close completed iteration acceptance done remaining work"],"multi-tenant-isolation-audit":["tenant isolation cross tenant data authorization"],"multi-tenant-isolation-polish":["fix tenant isolation cross tenant data authorization"],"tenant-isolation-check":["verify tenant isolation cross tenant data authorization"]},"goal_routes":[{"subjects":["website","site","homepage","landing page","web site","сайт","сайта","сайтик","лендинг","лендинга","главную страницу","главную сайта","главную","главная страница","sitio web","página de inicio","página de destino","网站","首页","落地页","сайте","сайту","сайтом","главная","главной","sitio","portada","网页"],"goals":[{"id":"web-offer-synthesis","phrases":["сначала понять предложение","сначала нужно понять предложение","сначала продумать предложение","продумать предложение","нужна концепция","figure out the offer","define the offer","definir la oferta","先明确定位"],"prefer":true},{"id":"web-project-architecture","phrases":["архитектура сайта","архитектуру сайта","архитектура проекта","какой стек","из чего собрать","как разложить код","модульную структуру","project architecture","site architecture","architecture of the site","what stack","structure the codebase","arquitectura del sitio","qué tecnología","qué stack","网站架构","技术栈","怎么组织代码"],"prefer":true},{"id":"web-page-architecture","phrases":["какие разделы","какие блоки нужны","структуру главной","как построить главную","what sections","which sections","how should the homepage be structured","qué secciones","qué apartados","cómo estructurar la portada","哪些板块","哪些栏目"],"prefer":true},{"id":"homepage-landing-polish","phrases":["доделай сайт","переделай сайт","улучши главную","переделай главную","доделай лендинг","finish the website","improve the homepage","redesign the homepage","rediseñar la portada","mejora la página de inicio","改版首页","完善网站"],"prefer":true},{"id":"homepage-landing-audit","phrases":["разваливается на телефоне","ломается на телефоне","съезжает на мобильном","выглядит дешево","looks cheap","falls apart on mobile","broken on mobile","se rompe en el móvil","se ve mal en el móvil","手机上乱了","手机上错位","看起来廉价"],"prefer":true},{"id":"homepage-landing-build","phrases":["сделай сайт","сделай мне сайт","создай сайт","сделать сайт","создать сайт","собрать сайт","собери лендинг","сделай красивый сайт","сделай мне красивый сайт","сделать красивый сайт","хочу красивый сайт","нужен красивый сайт","сделай современный лендинг","build a website","build a landing page","create a website","make a website","make a beautiful site","make me a beautiful website","make a beautiful website","quiero crear un sitio web","hazme un sitio web bonito","hazme una web bonita","做个漂亮的网站","做一个漂亮的网站","给我做个网站"],"prefer":true},{"id":"web-offer-synthesis","phrases":["сначала понять","сначала нужно понять","сначала продумать","продумать предложение","нужна концепция","пока только план","proposal","plan first","oferta","先规划"]},{"id":"homepage-landing-polish","phrases":["доделай","доделать","довести до ума","переделай","переделать","обнови дизайн","redesign","finish","rediseñar","terminar","改版","完善"]},{"id":"homepage-landing-build","phrases":["сделай","создай","собери","нужен красивый","хочу красивый","build","create","make","crear","construir","创建","搭建"]}]},{"subjects":["бэкэнд","бэкенд","бекенд","бэкенда","бэкенде","сервер","сервере","backend","back end","api","servidor","servicio","后端","服务器","接口"],"goals":[{"id":"instant-backend-probe","phrases":["глючит","зависает","не отвечает","ответ не приходит","ответ так и не приходит","висит и","висит без ответа","never responds","stops responding","hang","hangs","stalls","gets stuck","no responde","se queda cargando","se cuelga","一直转圈","没有响应","卡住"],"prefer":true}]},{"subjects":["база данных","базе","базу","таблица","таблицу","database","table","base de datos","tabla","数据库","数据表"],"goals":[{"id":"sql-databases-audit","phrases":["добавить обязательное поле","добавить поле без простоя","обязательное поле","без остановки сервиса","add a required column","add a column without downtime","change the schema without downtime","añadir una columna obligatoria","sin parar el servicio","添加必填字段","不停机修改表结构","zero downtime","required database field","adding a required field","no downtime"],"prefer":true}]},{"subjects":["роль","роли","ролью","права","доступ","role","permissions","access","rol","permisos","角色","权限"],"goals":[{"id":"rbac-abac-policy-audit","phrases":["после смены роли","роль изменилась","доступ остался","все еще видит закрытые записи","бывшая роль","after a role change","still has access","permissions did not update","después de cambiar de rol","sigue teniendo acceso","角色变更后","权限未更新","还能看到受限记录","role changed","stale permissions","still see restricted records"],"prefer":true}]},{"subjects":["тесты","тест","проверки","tests","test","pruebas","测试"],"goals":[{"id":"test-coverage-audit","phrases":["то проходят то падают","случайно падают","падают без правок","нестабильные тесты","pass and fail without changes","fail intermittently","flaky tests","nondeterministic tests","fallan de forma intermitente","pruebas inestables","时过时不过","偶尔失败","结果不稳定","intermittent test failures","tests fail randomly","иногда падают","не всегда проходят"],"prefer":true}]},{"subjects":["патч","правка","правку","изменения","коммит","patch","changes","pull request","commit","cambios","parche","改动","补丁","diff","дифф","изменение"],"goals":[{"id":"patch-checking","phrases":["до слияния","перед слиянием","можно ли вливать","что может сломаться после","before merging","safe to merge","review my changes","what could break after this change","antes de fusionar","revisa mis cambios","合并前","能否合并","检查这次改动","review this diff","перед мерджем"],"prefer":true}]},{"subjects":["новую возможность","новую функцию","релиз","выкатить","new feature","release","rollout","funcionalidad","nueva función","lanzamiento","新功能","发布","feature"],"goals":[{"id":"feature-flags-rollout-audit","phrases":["части пользователей","по группам","по частям","не всем сразу","быстро выключить","subset of users","fraction of users","gradual rollout","turn it off quickly","gradually enable","parte de los usuarios","por grupos","desactivar rápidamente","分批","部分用户","快速关闭","limited user cohort","kill switch","percentage of users"],"prefer":true}]},{"subjects":["приложение","приложения","клиент","клиента","ответ","ответа","api","application","client","response","aplicación","cliente","respuesta","应用","客户端","接口","响应"],"goals":[{"id":"api-contract-compatibility-check","phrases":["перестала получать привычные поля","пропали поля","совместимость ответа","сломали совместимость","older client stopped receiving","response fields disappeared","backward compatibility","faltan campos en la respuesta","compatibilidad con versiones anteriores","旧版缺少字段","向后兼容","字段消失","backwards compatibility","missing response fields","response fields removed"],"prefer":true}]}]};
