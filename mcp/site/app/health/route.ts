import {libraryStatus} from '../../lib/vibe/metadata.js';
export function GET() {return Response.json(libraryStatus(), {headers: {'Cache-Control': 'no-store'}});}
