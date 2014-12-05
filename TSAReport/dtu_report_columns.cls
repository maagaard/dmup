\LoadClass[a4paper,10pt]{IEEEtran}

% \pdfoutput=1

%-------- RequirePackages
\RequirePackage{subfiles}
\RequirePackage{listings}
\RequirePackage{graphicx}
\RequirePackage{hyperref}
\RequirePackage[parfill]{parskip}

\RequirePackage{marvosym}
\RequirePackage{wasysym}
\RequirePackage{latexsym}
\RequirePackage{amssymb}

% - From FN
\RequirePackage[utf8]{inputenc}
\RequirePackage[table]{xcolor}
\RequirePackage{pdfpages}



%-------- Include
\include{language_defs}


%-------- Package settings
\graphicspath{ {./figures/} }




%-------- Page setup
\textwidth 16cm
\textheight 22cm
\oddsidemargin 0cm
\topmargin -1cm
\def\x{{\bf x}}
\def\w{{\bf w}}
\def\squeeze{\itemsep=0pt\parskip=0pt}

% - From FN
\hypersetup{colorlinks=true,citecolor=[rgb]{0,0.4,0}}