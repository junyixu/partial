" TODO
" 部分公式预览
function g:PreviewEq4LaTeX()
if g:asyncrun_status!='running'
	silent normal mz"xyie
	" TODO latex_img 目录由 ueberzug_latex.py 创建，导致第一次 writefile
	" 无法写入 formula.txt，紧接着 ueberzug_latex.py 无法 cat formula.txt
	call writefile(getreg('x',1,1), '/tmp/latex_img/formula.txt')
	normal `z
	normal mz
	AsyncRun -silent ~/.vim/scripts/ueberzug_latex.py
else
	AsyncStop
endif
endfunction
function ScreenLine()
	" 当前行
	let a=line(".")
	" 屏幕首行
	let b=line("w0")
 return a - b - 2
endfunction
function ScreenColumn()
 return col(".") + 20
endfunction
function g:VisualPreviewEq4LaTeX()
	call writefile(getreg('*',1,1), '/tmp/latex_img/formula.txt')
	AsyncRun -silent ~/.vim/scripts/ueberzug_latex.py
endfunction
nnoremap <silent><buffer> <space><space> :call g:PreviewEq4LaTeX()<cr>
vnoremap <silent><buffer> <CR> :call g:VisualPreviewEq4LaTeX()<cr>
