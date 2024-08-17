function gdoc#LoadCommand(plug_path, path_to_creds, token_directory, gdoc_path, opts)
    call gdoc#Gdoc(a:plug_path, a:path_to_creds, a:token_directory, a:gdoc_path)
    let args = split(a:opts, ' ')
    let mode = args[0]

    if mode  == 'write'
        call gdoc#WriteDoc()
    elseif mode  == 'sync'
        call gdoc#Sync()
    elseif mode  == 'sync-doc'
        call gdoc#SyncDoc()
    elseif mode  == 'rm'
        call gdoc#RmDoc()
    elseif mode == 'fetch-doc'
        if len(args) <= 1
            echoerr "gdoc.vim: fetch-doc expects a document id"
        else
            call gdoc#FetchDoc(args[1])
        endif
    else
        echoerr "Exaustive handling of Arguments; " . mode . " Not found"
    endif
endfunction

function gdoc#Gdoc(plug_path, path_to_creds, token_directory, gdoc_path)
  python3 << EOF
import vim
import sys
from os.path import normpath, join, expanduser

plugin_root_dir = vim.eval('a:plug_path')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

from gdoc import doc_query
from fmt_msg import GdocErr

creds_path = expanduser(vim.eval('a:path_to_creds'))
token_path = expanduser(vim.eval('a:token_directory'))
gdoc_path = expanduser(join(vim.eval('a:gdoc_path'), '.gdoc'))

query = doc_query(creds_path, token_path, gdoc_path)

from gdoc_vim_utils import (
  doc_rm,
  doc_sync_doc,
  doc_sync,
  doc_fetch,
  doc_write
)
EOF
endfunction

function gdoc#RmDoc()
  python3 << EOF
doc_rm(vim, query, GdocErr)
EOF
endfunction

function gdoc#SyncDoc()
  python3 << EOF
doc_sync_doc(vim, query, GdocErr)
EOF

:edit!
endfunction

function gdoc#Sync()
  python3 << EOF
doc_sync(vim, query, GdocErr)
EOF
endfunction

function gdoc#WriteDoc()
  python3 << EOF
doc_write(vim, query, GdocErr)
EOF
endfunction

function gdoc#FetchDoc(doc_id)
  python3 <<EOF
doc_fetch(vim, query, GdocErr)
EOF
endfunction
