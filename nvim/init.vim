call plug#begin('~/.vim/plugged')

Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'scrooloose/nerdtree'
Plug 'tsony-tsonev/nerdtree-git-plugin'
"Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'ryanoasis/vim-devicons'
Plug 'airblade/vim-gitgutter'
Plug 'ctrlpvim/ctrlp.vim' " fuzzy find files
Plug 'scrooloose/nerdcommenter'
Plug 'numirias/semshi'
Plug 'vim-airline/vim-airline'
Plug 'lervag/vimtex'
Plug 'sheerun/vim-polyglot'

call plug#end()

syntax on

let g:powerline_pycmd="py3"
let g:NERDTreeGitStatusWithFlags=1
let g:NERDTreeGitStatusNodeColorization = 1
let g:NERDTreeColorMapCustom = {
			\ "Staged"    : "#0ee375",  
			\ "Modified"  : "#d9bf91",  
			\ "Renamed"   : "#51C9FC",  
			\ "Untracked" : "#FCE77C",  
			\ "Unmerged"  : "#FC51E6",  
			\"Dirty"     : "#FFBD61",  
			\"Clean"     : "#87939A",   
			\"Ignored"   : "#808080"   
			\ }

let g:NERDTreeIgnore = ['^node_modules$']

command! -nargs=0 Prettier :CocCommand prettier.formatFile


let g:ctrlp_user_command = ['.git/', 'git --git-dir=%s/.git ls-files -oc --exclude-standard']
let g:vimtex_view_method = 'zathura'
"let g:airline#extensions#tabline#enabled = 1

set smarttab
set cindent
set nowrap
set mouse=a
set whichwrap=b,s,<,>,[,]

set number relativenumber

set grepprg=grep\ -nH\ $*
let g:tex_flavor = "latex"

nmap <C-n> :NERDTreeToggle<CR>

nnoremap p "+p
nnoremap y "+y

autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | exe 'cd '.argv()[0] | endif


function! SyncTree()
  if &modifiable && IsNERDTreeOpen() && strlen(expand('%')) > 0 && !&diff
    NERDTreeFind
    wincmd p
  endif
endfunction

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction


" gopass setting - dont store text passwords in temp files
"au BufNewFile,BufRead /dev/shm/gopass.* setlocal noswapfile nobackup noundofile
