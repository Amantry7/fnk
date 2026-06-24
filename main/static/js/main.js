(function () {
    'use strict';

    /* ---------- Header scroll state ---------- */
    var header = document.getElementById('siteHeader');
    var toTop = document.querySelector('.to-top');
    function onScroll() {
        var y = window.scrollY || window.pageYOffset;
        if (header) header.classList.toggle('scrolled', y > 30);
        if (toTop) toTop.classList.toggle('show', y > 600);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ---------- Mobile menu ---------- */
    var burger = document.getElementById('burger');
    var nav = document.getElementById('nav');
    function closeMenu() {
        if (!nav || !burger) return;
        nav.classList.remove('open');
        burger.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
    }
    if (burger && nav) {
        burger.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            burger.classList.toggle('open', open);
            burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        nav.querySelectorAll('a').forEach(function (a) {
            a.addEventListener('click', closeMenu);
        });
    }

    /* ---------- Reveal on scroll ---------- */
    var reveals = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        reveals.forEach(function (el, i) {
            el.style.transitionDelay = (Math.min(i % 4, 3) * 0.08) + 's';
            io.observe(el);
        });
    } else {
        reveals.forEach(function (el) { el.classList.add('visible'); });
    }

    /* ---------- Animated counters ---------- */
    function animateCount(el) {
        var target = parseFloat(el.getAttribute('data-target')) || 0;
        var prefix = el.getAttribute('data-prefix') || '';
        var suffix = el.getAttribute('data-suffix') || '';
        var dur = 1400, start = null;
        function frame(ts) {
            if (!start) start = ts;
            var p = Math.min((ts - start) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            var val = target * eased;
            var shown = Number.isInteger(target) ? Math.round(val) : val.toFixed(1);
            el.textContent = prefix + shown + suffix;
            if (p < 1) requestAnimationFrame(frame);
            else el.textContent = prefix + target + suffix;
        }
        requestAnimationFrame(frame);
    }
    var counters = document.querySelectorAll('.count');
    if (counters.length && 'IntersectionObserver' in window) {
        var cio = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
            });
        }, { threshold: 0.5 });
        counters.forEach(function (c) { cio.observe(c); });
    } else {
        counters.forEach(animateCount);
    }

    /* ---------- FAQ accordion ---------- */
    document.querySelectorAll('.faq-item').forEach(function (item) {
        var q = item.querySelector('.faq-q');
        var a = item.querySelector('.faq-a');
        q.addEventListener('click', function () {
            var isOpen = item.classList.contains('open');
            document.querySelectorAll('.faq-item.open').forEach(function (other) {
                if (other !== item) {
                    other.classList.remove('open');
                    other.querySelector('.faq-a').style.maxHeight = null;
                }
            });
            if (isOpen) {
                item.classList.remove('open');
                a.style.maxHeight = null;
            } else {
                item.classList.add('open');
                a.style.maxHeight = a.scrollHeight + 'px';
            }
        });
    });

    /* ---------- Pricing plan -> form ---------- */
    var planSelect = document.getElementById('id_plan');
    document.querySelectorAll('[data-plan]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            if (planSelect) planSelect.value = btn.getAttribute('data-plan');
        });
    });

    /* ---------- AJAX form submit ---------- */
    var form = document.getElementById('consultForm');
    if (form) {
        var result = document.getElementById('formResult');
        var submitBtn = document.getElementById('submitBtn');

        function getCookie(name) {
            var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
            return m ? m.pop() : '';
        }
        function clearErrors() {
            form.querySelectorAll('.field-error').forEach(function (el) {
                el.textContent = ''; el.classList.remove('show');
            });
            form.querySelectorAll('.field.invalid').forEach(function (el) {
                el.classList.remove('invalid');
            });
        }
        function showErrors(errors) {
            Object.keys(errors).forEach(function (key) {
                var box = form.querySelector('.field-error[data-for="' + key + '"]');
                if (box) {
                    box.textContent = errors[key].join(' ');
                    box.classList.add('show');
                    var field = box.closest('.field');
                    if (field) field.classList.add('invalid');
                }
            });
        }

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            clearErrors();
            if (result) { result.textContent = ''; result.className = 'form-result'; }
            submitBtn.disabled = true;
            var original = submitBtn.textContent;
            submitBtn.textContent = 'Отправляем…';

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new FormData(form)
            })
            .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
            .then(function (res) {
                if (res.ok && res.data.ok) {
                    form.reset();
                    if (result) { result.textContent = res.data.message; result.className = 'form-result ok'; }
                } else {
                    if (res.data.errors) showErrors(res.data.errors);
                    if (result) { result.textContent = 'Проверьте поля формы и попробуйте снова.'; result.className = 'form-result err'; }
                }
            })
            .catch(function () {
                if (result) { result.textContent = 'Ошибка отправки. Попробуйте позже или позвоните нам.'; result.className = 'form-result err'; }
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.textContent = original;
            });
        });
    }

    /* ---------- Footer year fallback / smooth anchor offset handled by CSS ---------- */
})();
