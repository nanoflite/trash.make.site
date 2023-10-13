BEGIN { 
    refcnt=1;
    preformat=0;
}

/^```/ { 
    preformat=!preformat;
    sub(/^```/, "");
}

{

    if (preformat) {
        sub(/^\s+/, "  ");
        print $0;
        next;
     }


    sub(/^\s+/, "");
    sub(/\t/, "  ");

 	while(match($0, /!\[[^\]]*\]\([^\)]*\)/)){
 		split(substr($0, RSTART, RLENGTH), a, /(!\[)|\)|(\]\()/);
        if (a[3]~/\.gif$/) {
 		    sub(/!\[[^\]]+\]\([^\)]+\)/, "g"a[2]"\t"a[3]);
        } else {
 		    sub(/!\[[^\]]+\]\([^\)]+\)/, "I"a[2]"\t"a[3]);
        }      
 	}

    while(match($0, /[^!]?\[[^\]]*\]\([^\)]*\)/)) { 
		split(substr($0, RSTART, RLENGTH), a, /[\[\)]|(\]\()/);
        if (a[3]~"^http|mailto") {
            refs[refcnt]="h[ref#"refcnt"] "a[2]"\tURL:"a[3];
        } else {
            refs[refcnt]="1[ref#"refcnt"] "a[2]"\t"a[3];
        }
		sub(/\[[^\]]+\]\([^\)]+\)/, a[2]" (ref#"refcnt++")");
    }

    $0 = gensub(/^#+\s*(.*)$/, "// \\1 //", "g");
    $0 = gensub(/\*+([^\*]+)\*+/, "\\1", "g");

    partcnt=split($0,parts,/\s+/);
     l=0;
     for(x=1;x<=partcnt;x++) {
         l=l+length(parts[x])+1
         if (l>65) {
             printf "\n";
             l=0;
         }
         printf "%s ",parts[x]
     }
     print "";

}

END {

    if (refcnt>0) {
        print ""
        print "// Table of refs //"
        print ""

        for (x=1; x <= refcnt; x++)
            print refs[x]
    }
}
