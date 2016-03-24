FILES :=                              \
    .travis.yml                       \
    apiary.apib                       \
    IDB1.log                          \
    models.html                       \
    models.py                         \
    tests.py                          \
    UML.pdf                           \

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -rf netflix-tests

status:
	make clean
	@echo
	git branch
	git remote -v
	git status
