export default {
  async fetch(request, env, ctx) {
    const event = await request.json();
    env.STORE.put(event.id, event.value);
    return new Response('Saved', { status: 201 });
  }
};
