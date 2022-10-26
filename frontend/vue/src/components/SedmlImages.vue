<template>
    <v-container fluid>
      <v-row 
        dense
        class="a-1 ma-1"
      >
      <div align="center" style="margin-right:10px;">
        <img 
          v-for="plot, i in getSedmlList"
          :key="i"
          :src="plot.url"
          height="auto"
          :width="width"
          class="style_prevu_kit"
        >
      </div>
      </v-row>
    </v-container>
</template>

<script>
  export default {
    name: 'sedml-images',
    props: ['sedmls', 'width'],
    computed:{
      getSedmlList(){
        let result = []
        for(const i in this.sedmls){
          result = result.concat(this.sedmls[i].plots)
        }
        return result
      },
    },
  }
</script>

<style>
.style_prevu_kit
{
    display:inline-block;
    border:0;
    position: relative;
    -webkit-transition: all 200ms ease-in;
    -webkit-transform: scale(1); 
    -ms-transition: all 200ms ease-in;
    -ms-transform: scale(1); 
    -moz-transition: all 200ms ease-in;
    -moz-transform: scale(1);
    transition: all 200ms ease-in;
    transform: scale(1);   
}
.style_prevu_kit:hover
{
    box-shadow: 0px 0px 150px #000000;
    z-index: 2;
    -webkit-transition: all 200ms ease-in;
    -webkit-transform: scale(2.5);
    -ms-transition: all 200ms ease-in;
    -ms-transform: scale(2.5);   
    -moz-transition: all 200ms ease-in;
    -moz-transform: scale(2.5);
    transition: all 200ms ease-in;
    transform: scale(2.5);
    background-color: white;
    position:absolute;
}
</style>