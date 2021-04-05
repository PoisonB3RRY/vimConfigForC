:set nu "设置显示行号
:set backspace=2 "能使用backspace回删
:syntax on "语法检测
:set ruler "显示最后一行的状态
:set bg=dark "背景色设置
:set hlsearch "高亮度反白
:set laststatus=2 "两行状态行+一行命令行
:set cindent "设置c语言自动对齐
:set t_Co=256 "指定配色方案为256
":set mouse=a "设置可以在VIM使用鼠标
:set tabstop=4 "设置TAB宽度
:set softtabstop=4
:set shiftwidth=4
:set expandtab
:set history=1000 "设置历史记录条数
:set nocompatible "设置不兼容

inoremap ' ''<ESC>i
inoremap " ""<ESC>i
inoremap ( ()<ESC>i
inoremap [ []<ESC>i
inoremap { {<CR>}<ESC>O


"PATHOGEN配置
:call pathogen#infect()
:filetype plugin on "允许插件
:filetype plugin indent on "启动智能补全

"快捷键:使用F3打开关闭
map <F3> :NERDTreeMirror <CR> 
map <F3> :NERDTreeToggle <CR>  
""NERDTree配置  
let NERDChristmasTree=1 "显示增强
let NERDTreeAutoCenter=1 "自动调整焦点
let NERDTreeShowFiles=1 "显示文件
let NERDTreeShowLineNumbers=1 "显示行号
let NERDTreeHightCursorline=1 "高亮当前文件
let NERDTreeShowHidden=0 "显示隐藏文件
let NERDTreeMinimalUI=0 "不显示'Bookmarks' label 'Press ? for help'
let NERDTreeWinSize=31 "窗口宽度

"配置Supertab
"let g:SuperTabRetainCompletionType=2 "记住上次的补全方式,直到按Esc退出插入模式位置
"let g:SuperTabDefaultCompletionType="<c-x><c-o>"  "按下tab后默认补全方式为<c-p>,现在改为<c-x><c-o>

"taglist配置信息
let Tlist_Auto_Open=1 " Let the tag list open automatically
let Tlist_Auto_Update=1 " Update the tag list automatically
let Tlist_Compact_Format=1 " Hide help menu
let Tlist_Ctags_Cmd='ctags' " Location of ctags
let Tlist_Enable_Fold_Column=0 "do show folding tree
let Tlist_Process_File_Always=1 " Always process the source file
let Tlist_Show_One_File=1 " Only show the tag list of current file
let Tlist_Exist_OnlyWindow=1 " If you are the last, kill yourself
let Tlist_File_Fold_Auto_Close=0 " Fold closed other trees
let Tlist_Sort_Type="name" " Order by name
let Tlist_WinWidth=30 " Set the window 40 cols wide.
let Tlist_Close_On_Select=1 " Close the list when a item is selected
let Tlist_Use_SingleClick=1 "Go To Target By SingleClick
let Tlist_Use_Right_Window=1 "在右侧显示
"打开关闭快捷键
map <silent> <F2> :TlistToggle<CR> 

" 配置YCM
let g:ycm_server_python_interpreter='/usr/bin/python'
let g:ycm_global_ycm_extra_conf='~/.vim/.ycm_extra_conf.py'
