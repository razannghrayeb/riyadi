



document.addEventListener('DOMContentLoaded',function(){


    document.querySelector('#LeipzigFocus').addEventListener('mouseenter',function(){
        this.classList.add('focus');
    });

    document.querySelector('#LeipzigFocus').addEventListener('mouseleave',function(){
        this.classList.remove('focus');
    });
});