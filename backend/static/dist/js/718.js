"use strict";(self["webpackChunkfrontendaa"]=self["webpackChunkfrontendaa"]||[]).push([[718],{4718:function(t,e,s){s.r(e),s.d(e,{default:function(){return k}});var r=s(821);const i={class:"stock-prices-container"},c=(0,r._)("h1",{class:"title"},"Current Prices",-1),a={class:"stock-data"},o={class:"box"};function n(t,e,s,n,l,p){return(0,r.wg)(),(0,r.iD)("div",i,[c,(0,r._)("div",a,[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(l.latestCryptoPrices,((t,e)=>((0,r.wg)(),(0,r.iD)("div",{class:"stock-container",key:t},[(0,r._)("div",o,(0,r.zw)(e)+" - $"+(0,r.zw)(t.USD),1)])))),128))])])}s(7658);var l=s(196),p=s(7202),u={name:"StockPrices",data(){return{latestCryptoPrices:[]}},mounted(){this.getLatestCryptoPrices(),document.title="Crypto Prices | StockApp",this.price_update_timer=setInterval((()=>{console.log("Set timer to recieve stock data every 5 sec"),this.getLatestCryptoPrices()}),5e3)},methods:{async getLatestCryptoPrices(){if(!this.$store.state.isAuthenticated)return clearInterval(this.timer),void p.Z.push("/");console.log("Updating crypto prices..."),await l.ZP.get("/api/stocks/").then((t=>{200!==t.status&&this.$store.refreshToken(),this.latestCryptoPrices=t.data})).catch((t=>{console.log(t),this.verifyToken()}))}},unmounted(){console.log("niszcze price_update_timer"),clearInterval(this.price_update_timer)}},d=s(3744);const h=(0,d.Z)(u,[["render",n]]);var k=h}}]);
//# sourceMappingURL=718.js.map