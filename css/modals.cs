@import url(http://fonts.googleapis.com/css?family=Modern+Antiqua);
/*---------------------------------------------------
    LESS Elements 0.9
  ---------------------------------------------------
    A set of useful LESS mixins
    More info at: http://lesselements.com
  ---------------------------------------------------*/
.clearfix {
  zoom: 1;
}
.clearfix:before {
  content: '';
  display: block;
}
.clearfix:after {
  content: '';
  display: table;
  clear: both;
}
/*@modalheight: 480px;*/
/*@modalwidth: 960px;*/
/*@font-face {*/
/*font-family: "HandShop";*/
/*src: url('../fonts/HandShop.ttf');*/
/*}*/
@font-face {
  font-family: "Parisish";
  src: url('../fonts/Parisish.ttf');
}
#modal-overlay {
  min-width: 100%;
  min-height: 100%;
  z-index: 999;
  background-color: rgba(0, 0, 0, 0.8);
  position: fixed;
  top: 0;
  left: 0;
  padding: 0;
}
#modal-frame {
  min-width: 80%;
  min-height: 80%;
  width: 80%;
  height: 80%;
  background-color: rgba(183, 242, 0, 0);
  position: absolute;
  left: 50%;
  top: 50%;
  margin-left: -38%;
  margin-top: -20%;
  zoom: 1;
  padding: 0;
}
#modal-frame:before {
  content: '';
  display: block;
}
#modal-frame:after {
  content: '';
  display: table;
  clear: both;
}
#left-modal {
  z-index: 1001;
  width: 35%;
  min-width: 35%;
  height: 70%;
  min-height: 70%;
  position: absolute;
  margin-left: -5%;
  margin-top: 7.5%;
  background-color: #ef002a;
  -webkit-border-top-right-radius: 0;
  -webkit-border-bottom-right-radius: 0;
  -webkit-border-bottom-left-radius: 40px;
  -webkit-border-top-left-radius: 40px;
  -moz-border-radius-topright: 0;
  -moz-border-radius-bottomright: 0;
  -moz-border-radius-bottomleft: 40px;
  -moz-border-radius-topleft: 40px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 40px;
  border-top-left-radius: 40px;
  -moz-background-clip: padding-box;
  -webkit-background-clip: padding-box;
  background-clip: padding-box;
  background-image: url('../images/modal-left-1.jpg');
  background-size: cover;
  padding: 0;
  box-shadow: inset 0 0 32px 8px rgba(0, 0, 0, 0.3);
}
h3.modaltitle {
  font-family: Bellerose, sans-serif;
  font-weight: 800;
  letter-spacing: -4px;
  word-spacing: -12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 70px;
  line-height: 84px;
  position: relative;
  top: -11.200000000000001px;
  margin: 0;
}
.modaltitleholder {
  width: 100%;
  background: rgba(0, 0, 0, 0.4);
  text-align: center;
  position: absolute;
  bottom: 50%;
  margin-bottom: -35px;
}
.modalmenu {
  position: absolute;
  top: 54%;
  margin-top: 35px;
  background: rgba(0, 0, 0, 0.3);
  text-transform: uppercase;
  width: 100%;
  padding: 8px 0 8px 0;
}
.modalmenu ul {
  list-style: none;
  margin: 0 auto;
  padding: 0;
}
.modalmenu li {
  font-family: Bellerose, sans-serif;
  font-weight: 400;
  font-size: 18px;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 18px;
  float: left;
  text-align: center;
}
#right-modal {
  z-index: 1002;
  width: 70%;
  min-width: 70%;
  height: 100%;
  min-height: 100%;
  /*background-color: @color1; */

  position: absolute;
  right: 0;
  top: 0;
  -webkit-border-radius: 40px;
  -moz-border-radius: 40px;
  border-radius: 40px;
  box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.8);
  /*background-image: -webkit-radial-gradient(circle 1200px at -400px -200px, fade(white, 2%) 98%, rgba(255, 255, 255, 0) 100%);*/

  /*background-image: radial-gradient(circle 1200px at -200px -700px, fade(white, 2%) 99%, rgba(255, 255, 255, 0) 100%);*/

  /*box-shadow: 0 0 5px 2px fade(black, 60%), inset 0 0 6px fade(white, 15%);*/

  /*background-image: -webkit-linear-gradient( rgba(255, 255, 255, 0.2) ), @rightbg;*/

  /*background-image: linear-gradient( rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7) ), @rightbg;*/

  /*background-size: cover;*/

  /*background-position: center center;*/

  background-image: -webkit-radial-gradient(circle 1200px at -100px -100px, #ef002a, #ff2800);
  background-image: radial-gradient(circle 1200px at -100px -100px, #ef002a, #ff2800);
}
#right-modal div.content {
  position: absolute;
  top: 75px;
  color: rgba(0, 0, 0, 0.8);
  padding: 0 32px 0 32px;
  font-size: 18px;
  font-family: 'Modern Antiqua', serif;
  overflow: auto;
}
.modaltopmenu {
  position: absolute;
  top: 0;
  width: 100%;
  height: 75px;
  /*min-width: 100%;*/

  /*min-height: @modaltopmenuheight;*/

  background: rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
  -moz-box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
}
.modaltopmenu ul {
  list-style: none;
  margin: 0 auto;
  padding: 0;
  text-transform: uppercase;
}
.modaltopmenu li {
  font-family: Bellerose, sans-serif;
  font-weight: 600;
  font-size: 18px;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.7);
  float: left;
  text-align: center;
  height: 100%;
  padding-top: 28.5px;
  cursor: pointer;
  cursor: hand;
}
.modaltopmenu li.active {
  border-bottom: medium solid #ff2800;
}
.modalbottommenu {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 75px;
  /*min-width: 100%;*/

  /*min-height: @modalbottommenuheight;*/

  background: rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
  -moz-box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
}
