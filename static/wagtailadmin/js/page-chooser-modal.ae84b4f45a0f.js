(()=>{"use strict";var t,e={8238:function(t,e,o){var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};e.__esModule=!0;var r=n(o(5311)),a=o(1460),i={browse:function(t,e){(0,r.default)(".link-types a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),wagtail.ui.initDropDowns(),(0,r.default)(".c-dropdown__item .u-link",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),t.ajaxifyForm((0,r.default)("form.search-form",t.body));var o,n=(0,r.default)("form.search-form",t.body).attr("action"),i=(0,r.default)(".page-results",t.body).html();function l(){var e=(0,r.default)("#id_q",t.body).val();return""!==e?o=r.default.ajax({url:n,data:{q:e},success:function(e){o=null,(0,r.default)(".page-results",t.body).html(e),u()},error:function(){o=null}}):((0,r.default)(".page-results",t.body).html(i),d()),!1}function u(){(0,r.default)(".page-results a.choose-page",t.body).on("click",(function(){var e=(0,r.default)(this).data();return t.respond("pageChosen",e),t.close(),!1})),(0,r.default)(".page-results a.navigate-pages, .page-results [data-breadcrumb-item] a",t.body).on("click",(function(){return(0,r.default)(".page-results",t.body).load(this.href,u),!1})),(0,r.default)(".page-results a.navigate-parent",t.body).on("click",(function(){return t.loadUrl(this.href),!1}))}function d(){(0,r.default)(".page-results a.navigate-pages, .page-results [data-breadcrumb-item] a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),(0,r.default)("a.choose-page",t.body).on("click",(function(){var o=(0,r.default)(this).data();return o.parentId=e.parent_page_id,t.respond("pageChosen",o),t.close(),!1})),(0,r.default)(".c-dropdown__item .u-link",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),wagtail.ui.initDropDowns()}(0,r.default)("#id_q",t.body).on("input",(function(){o&&o.abort(),clearTimeout(r.default.data(this,"timer"));var t=setTimeout(l,200);(0,r.default)(this).data("timer",t)})),d(),(0,a.initTooltips)(),(0,r.default)("#id_q",t.body).trigger("focus")},anchor_link:function(t){(0,r.default)("p.link-types a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),(0,r.default)("form",t.body).on("submit",(function(){return t.postForm(this.action,(0,r.default)(this).serialize()),!1}))},email_link:function(t){(0,r.default)("p.link-types a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),(0,r.default)("form",t.body).on("submit",(function(){return t.postForm(this.action,(0,r.default)(this).serialize()),!1}))},phone_link:function(t){(0,r.default)("p.link-types a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),(0,r.default)("form",t.body).on("submit",(function(){return t.postForm(this.action,(0,r.default)(this).serialize()),!1}))},external_link:function(t){(0,r.default)("p.link-types a",t.body).on("click",(function(){return t.loadUrl(this.href),!1})),(0,r.default)("form",t.body).on("submit",(function(){return t.postForm(this.action,(0,r.default)(this).serialize()),!1}))},external_link_chosen:function(t,e){t.respond("pageChosen",e.result),t.close()},confirm_external_to_internal:function(t,e){(0,r.default)("[data-action-confirm]",t.body).on("click",(function(){return t.respond("pageChosen",e.internal),t.close(),!1})),(0,r.default)("[data-action-deny]",t.body).on("click",(function(){return t.respond("pageChosen",e.external),t.close(),!1}))}};window.PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS=i},5311:t=>{t.exports=jQuery}},o={};function n(t){var r=o[t];if(void 0!==r)return r.exports;var a=o[t]={exports:{}};return e[t].call(a.exports,a,a.exports,n),a.exports}n.m=e,t=[],n.O=(e,o,r,a)=>{if(!o){var i=1/0;for(s=0;s<t.length;s++){for(var[o,r,a]=t[s],l=!0,u=0;u<o.length;u++)(!1&a||i>=a)&&Object.keys(n.O).every((t=>n.O[t](o[u])))?o.splice(u--,1):(l=!1,a<i&&(i=a));if(l){t.splice(s--,1);var d=r();void 0!==d&&(e=d)}}return e}a=a||0;for(var s=t.length;s>0&&t[s-1][2]>a;s--)t[s]=t[s-1];t[s]=[o,r,a]},n.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return n.d(e,{a:e}),e},n.d=(t,e)=>{for(var o in e)n.o(e,o)&&!n.o(t,o)&&Object.defineProperty(t,o,{enumerable:!0,get:e[o]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),n.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),n.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.j=726,(()=>{var t={726:0};n.O.j=e=>0===t[e];var e=(e,o)=>{var r,a,[i,l,u]=o,d=0;if(i.some((e=>0!==t[e]))){for(r in l)n.o(l,r)&&(n.m[r]=l[r]);if(u)var s=u(n)}for(e&&e(o);d<i.length;d++)a=i[d],n.o(t,a)&&t[a]&&t[a][0](),t[a]=0;return n.O(s)},o=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];o.forEach(e.bind(null,0)),o.push=e.bind(null,o.push.bind(o))})();var r=n.O(void 0,[751],(()=>n(8238)));r=n.O(r)})();