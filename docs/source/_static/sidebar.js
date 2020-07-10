+function(){
    
    var create = function(el, cls) {

            var element = document.createElement(el);

            element.classList.add(cls);

            return element;

        },

        link = function(target, text) {

            var id = text.replace(/[^\w]/, '-'),
                a = create('a', 'md-nav__link'),
                li = create('li', 'md-nav__item');

            target.setAttribute('id', id);
            a.href = `#${id}`;
            a.textContent = text;
            li.append(a);

            return li;

        },
    
        sidebar = function() {

            var container = document.querySelector('.md-sidebar--secondary .md-nav__list'),
                classes = document.querySelectorAll('dl.py.class');
            
            for (let i = 0; i < classes.length; ++i) {

                var _class = classes[i],    
                    navMethods = create('nav', 'md-nav'),
                    ulMethods = create('ul', 'md-nav__list'),
                    methods = _class.querySelectorAll('dl.py.method'),
                    className = _class.querySelector(':scope > dt > code.sig-name.descname').textContent,
                    liClass = link(_class, className);

                liClass.querySelector(':scope > a').classList.add('module-class');

                methods.forEach(function(_method) {

                    var methodName = _method.querySelector(':scope > dt > code.sig-name.descname').textContent + '()';
                    
                    ulMethods.append(link(_method, methodName));
                    
                });

                navMethods.append(ulMethods);
                liClass.append(navMethods);
                container.append(liClass);

            }

        };

    document.addEventListener('DOMContentLoaded', sidebar);

}();
