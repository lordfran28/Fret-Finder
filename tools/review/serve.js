const http=require('http'),fs=require('fs'),path=require('path');
const root=process.argv[2], T={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.mp3':'audio/mpeg','.jpg':'image/jpeg','.woff2':'font/woff2','.locked':'application/octet-stream','.svg':'image/svg+xml','.png':'image/png'};
http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0].split('#')[0]);let f=path.join(root,u);if(f.endsWith('/'))f+='index.html';
fs.stat(f,(e,st)=>{if(e||st.isDirectory()){r.writeHead(404);return r.end();}const ty=T[path.extname(f)]||'application/octet-stream';const rg=q.headers.range;
if(rg){const m=/bytes=(\d*)-(\d*)/.exec(rg);let s=m[1]?+m[1]:0,en=m[2]?+m[2]:st.size-1;r.writeHead(206,{'Content-Type':ty,'Content-Range':`bytes ${s}-${en}/${st.size}`,'Accept-Ranges':'bytes','Content-Length':en-s+1});fs.createReadStream(f,{start:s,end:en}).pipe(r);}
else{r.writeHead(200,{'Content-Type':ty,'Content-Length':st.size,'Accept-Ranges':'bytes'});fs.createReadStream(f).pipe(r);}});}).listen(+process.argv[3],'127.0.0.1');
