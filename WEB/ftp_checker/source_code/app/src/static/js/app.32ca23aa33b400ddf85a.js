webpackJsonp([1],{NHnr:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("7+uW"),r={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var s=a("VU/8")({name:"App"},r,!1,function(t){a("gsu9")},null,null).exports,l=a("/ocq"),o=a("mtWM"),i=a.n(o).a.create({baseURL:"/",timeout:5e3}),u=a("mw3O"),c=a.n(u);var p={data:function(){return{form:{input:""},result:""}},methods:{Submit:function(){var t,e=this;(t=this.form.input,i({url:"/ftpcheck",method:"post",headers:{"Content-Type":"application/x-www-form-urlencoded"},data:c.a.stringify({host:t})})).then(function(t){console.log(t.data),e.result=t.data})}}},d={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("el-row",[n("img",{staticClass:"logo",staticStyle:{width:"150px",height:"150px"},attrs:{src:a("tGse"),alt:""}}),t._v(" "),n("div",{staticClass:"h1"},[t._v("FTP CHECKER")])]),t._v(" "),n("el-row",{attrs:{type:"flex",justify:"center"}},[n("el-col",{attrs:{span:40}},[n("el-row",{staticClass:"row-bg",attrs:{gutter:"20",type:"flex"}},[n("div",[n("el-input",{staticStyle:{width:"400px"},attrs:{placeholder:"Host",clearable:""},model:{value:t.form.input,callback:function(e){t.$set(t.form,"input",e)},expression:"form.input"}}),t._v(" "),n("el-button",{staticClass:"n",attrs:{type:"danger"},on:{click:t.Submit}},[t._v("Submit")])],1)]),t._v(" "),n("el-row",{staticClass:"row-bg",attrs:{gutter:"20",type:"flex"}},[n("el-input",{staticStyle:{width:"500px"},attrs:{type:"textarea",rows:10,placeholder:"Result"},model:{value:t.result,callback:function(e){t.result=e},expression:"result"}})],1)],1)],1)],1)},staticRenderFns:[]};var f=a("VU/8")(p,d,!1,function(t){a("vMlJ")},"data-v-165c432a",null).exports;n.default.use(l.a);var v=new l.a({routes:[{path:"/",name:"HelloWorld",component:f}]}),m=a("zL8q"),h=a.n(m);a("tvR6");n.default.config.productionTip=!1,n.default.use(h.a),new n.default({el:"#app",router:v,components:{App:s},template:"<App/>"})},gsu9:function(t,e){},tGse:function(t,e,a){t.exports=a.p+"static/img/1.4641b05.jpg"},tvR6:function(t,e){},vMlJ:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.32ca23aa33b400ddf85a.js.map