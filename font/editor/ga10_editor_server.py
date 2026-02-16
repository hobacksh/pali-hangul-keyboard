#!/usr/bin/env python3
import json, os, subprocess
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit

ROOT = os.path.dirname(__file__)
FONT_ROOT = os.path.dirname(ROOT)
PARAMS = os.path.join(ROOT, 'ga10_editor_params.json')
BUILD = os.path.join(FONT_ROOT, 'build', 'build_v289_ga10_from_params.py')
FONT_OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV289_Ga10Editor.otf')
FONT_COPY = os.path.join(FONT_ROOT, 'output', 'PaliHangulV289_Ga10Editor.otf')

class H(SimpleHTTPRequestHandler):
    def _json(self, obj, code=200):
        b=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ('/','/editor'):
            self.path='/ga10_editor.html'
            return super().do_GET()
        if path=='/params':
            with open(PARAMS,'r',encoding='utf-8') as f: p=json.load(f)
            return self._json(p)
        if path in ('/font.otf','/PaliHangulV289_Ga10Editor.otf'):
            try:
                with open(FONT_COPY,'rb') as f: b=f.read()
                self.send_response(200)
                self.send_header('Content-Type','font/otf')
                self.send_header('Content-Length',str(len(b)))
                self.end_headers()
                self.wfile.write(b)
                return
            except Exception as e:
                return self._json({'ok':False,'error':str(e)},404)
        return super().do_GET()

    def do_POST(self):
        if self.path=='/save':
            n=int(self.headers.get('Content-Length','0')); data=self.rfile.read(n)
            try:
                p=json.loads(data.decode('utf-8'))
                with open(PARAMS,'w',encoding='utf-8') as f: json.dump(p,f,ensure_ascii=False,indent=2)
                return self._json({'ok':True})
            except Exception as e:
                return self._json({'ok':False,'error':str(e)},500)
        if self.path=='/apply':
            try:
                env = os.environ.copy()
                env['OC_BUILD_TAG'] = str(int(__import__('time').time()))
                r=subprocess.run(['python3',BUILD],cwd=ROOT,capture_output=True,text=True,timeout=180,env=env)
                if r.returncode!=0:
                    return self._json({'ok':False,'error':r.stderr[-1200:],'out':r.stdout[-400:]},500)
                if os.path.exists(FONT_OUT):
                    subprocess.run(['cp',FONT_OUT,FONT_COPY],check=False)
                return self._json({'ok':True,'out':r.stdout[-400:]})
            except Exception as e:
                return self._json({'ok':False,'error':str(e)},500)
        return self._json({'ok':False,'error':'not found'},404)

if __name__=='__main__':
    os.chdir(ROOT)
    s=ThreadingHTTPServer(('127.0.0.1',39444),H)
    print('http://127.0.0.1:39444/editor')
    s.serve_forever()
