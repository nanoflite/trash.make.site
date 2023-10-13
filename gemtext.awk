BEGIN { 
    refcnt=0;
    preformat=0;
}

/^```/ { preformat=!preformat }

{
    if (preformat) {
        print $0;
        next;
    }

 	while(match($0, /!\[[^\]]+\]\([^\)]+\)/)){
 		split(substr($0, RSTART, RLENGTH), a, /(!\[)|\)|(\]\()/);
 		sub(/!\[[^\]]+\]\([^\)]+\)/, "=> "a[3]"  "a[2]);
 	}


    while(match($0, /[^!]?\[[^\]]*\]\([^\]]*\)/)) { 
		split(substr($0, RSTART, RLENGTH), a, /[\[\)]|(\]\()/);
        refs[++refcnt]="=> "a[3]"  "a[2]
		sub(/\[[^\]]+\]\([^\)]+\)/, a[2]" (ref#"refcnt")");
    }

    sub(/^\s+/, "");
    sub(/\t/, "  ");
    sub(/^###+/, "###")

    print $0
}

END {
    if (refcnt>0) {
        print ""
        print "# Table of refs:"
        print ""

        for (x=1; x <= refcnt; x++)
            print refs[x]
    }

}
