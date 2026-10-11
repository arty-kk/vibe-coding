import {libraryStatus} from '../../lib/vibe/library.js';
export function GET() {return Response.json(libraryStatus(), {headers: {'Cache-Control': 'no-store'}});}
