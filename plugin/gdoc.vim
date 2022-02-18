if !has('python3')
    echo "Error: Python3 is required for this to work. for more info, checkout https://github.com/aadv1k"
    finish
endif

let path_to_creds = get(g:, 'path_to_creds', "-1")
let token_directory = get(g:, 'token_directory', "-1")

if path_to_creds == -1
    echo "Please provde a credential file path."
    finish
endif

if token_directory == -1
    let token_directory = './'
endif

call doc#Gdoc(path_to_creds, token_directory)

let g:buf_content = join(getline(1,'$'), "\n")

command! -nargs=1 -complete=command Gdoc call doc#WriteDoc(<q-args>)
