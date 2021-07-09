%% Implemented by Martin Helsø (martibhe@math.uio.no)
%% Version: 23-09-2019
%%
%% Also available at:
%% https://github.com/martinhelso/uioposter

\NeedsTeXFormat{LaTeX2e}


\ProvidesClass{uioposter}


\DeclareOption{english}{\def\uioposter@lang{english}}

\DeclareOption{portrait}
{
    \PassOptionsToPackage{orientation = portrait}{beamerposter}
    \def\uioposter@orientation{}
}



\DeclareOption{a0paper}{\def\uioposter@size{a0paper}}
\DeclareOption{a4paper}{\def\uioposter@size{a4paper}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}


\ExecuteOptions{a0paper}
\ExecuteOptions{english}
\ExecuteOptions{portrait}
\ProcessOptions
\relax


\LoadClass[t]{beamer}


\RequirePackage[size = a0, scale = 1.5]{beamerposter}
\RequirePackage{etoolbox}
\RequirePackage{pgfpages}
\RequirePackage[T1]{fontenc}
\RequirePackage{calc}
\RequirePackage[final]{microtype}
\RequirePackage{lmodern}
\RequirePackage[scaled]{beramono}


\hypersetup{colorlinks,
            urlcolor  = uiolink,
            linkcolor =,
            citecolor =,
            filecolor =}
\renewcommand{\sfdefault}{phv}
\DeclareFontShape{OMX}{cmex}{m}{n}
{
    <-7.5>    cmex7
    <7.5-8.5> cmex8
    <8.5-9.5> cmex9
    <9.5->    cmex10
}{}
\SetSymbolFont{largesymbols}{normal}{OMX}{cmex}{m}{n}
\SetSymbolFont{largesymbols}{bold}  {OMX}{cmex}{m}{n}
\setlength{\marginparwidth}{2cm}
\setlength{\emergencystretch}{1em}
\frenchspacing

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usefonttheme{serif}
\useinnertheme{rectangles}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{caption}[numbered]
\setbeamertemplate{caption label separator}{: }
\setbeamertemplate{qed symbol}{\(\blacksquare\)}
\setbeamertemplate{itemize items}{\color{itemize item.fg}\(\blacksquare\)}


\setlength{\labelsep}{3ex}
\setlength{\leftmargini}{18ex}
\setbeamersize{text margin left = 5cm, text margin right = 5cm}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\definecolor{uiored}{HTML}{D3F8E2}
\definecolor{uiowhite}{HTML}{F0F5F9}
\definecolor{uioblack}{HTML}{000000}
\definecolor{uioheader}{HTML}{242038}
\definecolor{uiobackground}{HTML}{E7E5F0}
\definecolor{uiotertiary}{HTML}{EA1F4B}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamercolor{structure}{fg = uioheader}
\setbeamercolor{alerted text}{fg = uiored}
\setbeamercolor{background canvas}{fg = uiowhite, bg = uiobackground}
\setbeamercolor{headline}{fg = uiowhite, bg = uioheader}
\setbeamercolor{title in headline}{fg = uiored}
\setbeamercolor{author in headline}{fg = uiored}
\setbeamercolor{footline}{fg = uiowhite, bg = uioheader}


\setbeamercolor{block title}{fg = uiowhite, bg = uioheader}
\setbeamercolor{block title example}{fg = uiowhite, bg = uiotertiary}
\setbeamercolor{block title alerted}{fg = uiowhite, bg = uioheader}


\setbeamercolor{block body} {fg = uioblack, bg = uiowhite}
\setbeamercolor{block body example} {fg = uioblack, bg = uiowhite}
\setbeamercolor{block body alerted} {fg = uioblack, bg = uiowhite}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamerfont{title in headline}{family = \sffamily,
                                  series = \bfseries,
                                  size   = \Huge}
\setbeamerfont{author in headline}{family = \sffamily,
                                   series = \mdseries,
                                   size   = \large}
\setbeamerfont{institute}{family = \sffamily,
                          series = \mdseries,
                          size   = \normalsize}


\setbeamerfont{block title}{family = \sffamily,
                            series = \bfseries,
                            size   = \large}
\setbeamerfont{block title alerted}{family = \sffamily,
                                    series = \bfseries,
                                    size   = \large}
\setbeamerfont{block title example}{family = \sffamily,
                                    series = \bfseries,
                                    size   = \large}


\setbeamerfont{block body}{family = \rmfamily,
                           series = \normalfont,
                           size   = \normalsize}
\setbeamerfont{block body example}{family = \rmfamily,
                                   series = \normalfont,
                                   size   = \normalsize}
\setbeamerfont{block body alerted}{family = \rmfamily,
                                   series = \normalfont,
                                   size   = \normalsize}


\setbeamerfont{item projected}{family = \sffamily,
                               series = \bfseries,
                               size   = \small}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% \setbeamertemplate{headline}
% {
%     \begin{beamercolorbox}[wd = \paperwidth,
%                           leftskip  = 3cm,
%                           rightskip = 3cm plus 20cm]{headline}
%         \vskip-0.5cm
        
%         \begin{columns}[onlytextwidth]

%         \begin{column}{0.30\textwidth }
        
%         \includegraphics[width=1\textwidth]
%         {pic.png}
        
%         \end{column}
        
%         \begin{column}{0.001\textwidth}
        
%         \end{column}
        
        
%         \begin{column}{0.66\textwidth}
        
%         \usebeamerfont{title in headline}
%                 \usebeamercolor{title in headline}
%                 \color{fg}
%                 \vskip0ex
%                 \hskip-0.05ex
%                 \inserttitle
%                 \vskip1ex
%                 \usebeamerfont{author in headline}
%                 \usebeamercolor{author in headline}
%                 \color{fg}
%                 \hskip-0.05ex
%                 \insertauthor
%                 \ifdefempty{\insertinstitute}{}
%                 {
%                     \vskip1ex
%                     \usebeamerfont{institute}
%                     \def\beamer@andinst{\quad}
%                     \insertinstitute
%                 }
%                 \vskip3cm
        
%         \end{column}
        
        
%         \end{columns}

        
%     \end{beamercolorbox}
%     \vskip1cm
% }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{footline}
{
    \leavevmode
    \begin{beamercolorbox}[wd = \paperwidth]{footline}
        \vskip2cm
        \hskip4.1cm
        \vskip2cm
    \end{beamercolorbox}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block begin}
{
    \setbeamercolor{itemize item}  {fg = block title.bg}
    \setbeamercolor{item projected}{fg = block title.fg,
                                    bg = block title.bg}
    \setbeamercolor{description item}{fg = structure}

    \begin{beamercolorbox}[ht        = 3.2 ex,
                           dp        = 1.3 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex]
                          {block title}

        \usebeamerfont*{block title}
        \insertblocktitle
        
    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex,
                           vmode]
                          {block body}

        \usebeamerfont{block body}
        \vskip2ex
        \begin{minipage}{\textwidth-4ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
}


\setbeamertemplate{block end}
{
        \end{minipage}
    \vskip0.2ex
    \end{beamercolorbox}
    \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block example begin}
{
    \setbeamercolor{itemize item}  {fg = block title example.bg}
    \setbeamercolor{item projected}{fg = block title example.fg,
                                    bg = block title example.bg}
    \setbeamercolor{description item}{fg = structure}

    \begin{beamercolorbox}[ht        = 3.2 ex,
                           dp        = 1.3 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex]
                          {block title example}

        \usebeamerfont*{block title example}
        \insertblocktitle

    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex,
                           vmode]
                          {block body example}

        \usebeamerfont{block example body}
        \vskip2ex
        \begin{minipage}{\textwidth-4ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
}


\setbeamertemplate{block example end}
{
        \end{minipage}
    \vskip0cm
    \end{beamercolorbox}
    \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setbeamertemplate{block alerted begin}
{
    \setbeamercolor{itemize item}  {fg = block title alerted.bg}
    \setbeamercolor{item projected}{fg = block title alerted.fg,
                                    bg = block title alerted.bg}
    \setbeamercolor{description item}{fg = structure}

    \begin{beamercolorbox}[ht        = 3.2 ex,
                           dp        = 1.3 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex]
                          {block title alerted}

        \usebeamerfont*{block title alerted}
        \insertblocktitle

    \end{beamercolorbox}

    \nointerlineskip

    \begin{beamercolorbox}[dp        = 2 ex,
                           leftskip  = 2 ex,
                           rightskip = 2 ex,
                           vmode]
                          {block body alerted}

        \usebeamerfont{block body alerted}
        \vskip2ex
        \begin{minipage}{\textwidth-4ex}
             \setlength{\parskip}{1.5ex}
             \setlength{\abovecaptionskip}{1ex}
}


\setbeamertemplate{block alerted end}
{
        \end{minipage}
    \vskip0.2ex
    \end{beamercolorbox}
    \vskip3cm
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\enumitem}[1]
{{%
    \leavevmode\unskip
    \def\insertenumlabel{#1}
    \usebeamertemplate*{enumerate item}%
}}


\newcommand{\enumref}[1]{\enumitem{\ref{#1}}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\pgfpagesdeclarelayout{resize and center}
{
    \def\pgfpageoptionborder{0em}
}
{
    \pgfpagesphysicalpageoptions
    {
        logical pages   = 1,
        physical height = \pgfpageoptionheight,
        physical width  = \pgfpageoptionwidth
    }
    \pgfpageslogicalpageoptions{1}
    {
        resized width  = \pgfphysicalwidth,
        resized height = \pgfphysicalheight,
        border shrink  = \pgfpageoptionborder,
        center         = \pgfpoint{.5\pgfphysicalwidth}{.5\pgfphysicalheight}
    }
}


\ifdefstring{\uioposter@size}{a0paper}{}
{
    \pgfpagesuselayout{resize and center}[\uioposter@size,
                                          \uioposter@orientation]
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\endinput