<template>
  
  <div>
    
    <div v-if="math">
      <div 
        style="display: inline-block;"
        v-katex="math" ></div>
      <v-speed-dial
        v-model="fab"
        :top="false"
        :bottom="false"
        :absolute="true"
        :right="false"
        :left="false"
        :direction="'top'"
        :open-on-hover="true"
        :transition="'slide-y-transition'"
        style="display: inline-block;"
        v-if="math"
        >
        <template v-slot:activator>
          <v-btn
            v-model="fab"
            color="blue darken-2"
            dark
            icon
            x-small
            >
            <v-icon v-if="fab">
              mdi-close
            </v-icon>
            <v-icon v-else>
              mdi-content-copy
            </v-icon>
          </v-btn>
        </template>
        <v-tooltip left color="green">
          <template v-slot:activator="{ on }">
            <v-btn
            fab
            dark
            x-small
            color="green"
            @click="copyToClipBoard(math)"
            v-on="on"
            >
            CM
            <!-- <v-icon>mdi-pencil</v-icon> -->
            </v-btn>
          </template>
          <span>Copy math (LaTex)</span>
        </v-tooltip>
        <v-tooltip left color="indigo">
          <template v-slot:activator="{ on }">
            <v-btn
              fab
              dark
              x-small
              color="indigo"
              @click="copyToClipBoard(dependencies)"
              v-on="on"
              >
              <!-- <v-icon>mdi-plus</v-icon> -->
              CD
            </v-btn>
          </template>
          <span>Copy dependencies (LaTex)</span>
        </v-tooltip>
        <v-tooltip left color="red">
          <template v-slot:activator="{ on }">
            <v-btn
              fab
              dark
              x-small
              color="red"
              @click="copyToClipBoard(componentCode)"
              v-on="on"
              >
              CC
              <!-- <v-icon>mdi-delete</v-icon> -->
            </v-btn>
          </template>
          <span>Copy CellML</span>
        </v-tooltip>
      </v-speed-dial>
      <div>
        <v-expansion-panels flat v-if="dependencies">
          <v-expansion-panel class="elevation-0">
             <v-container class="ma-0 pa-0" fill-width fluid>
               <v-row class="ma-0 pa-0">
                 <v-col cols="4" class="ma-0 pa-0">
                   <v-expansion-panel-header class="ma-0 pa-0">
                     Dependencies
                   </v-expansion-panel-header>
                 </v-col>
                 <v-col cols="1"></v-col>
                 <v-col cols="6" class="ma-0 pa-0">
                   <v-switch  class="mt-2 pa-0"
                     v-model="showInit"
                     label="Show initial values"
                   ></v-switch>
                 </v-col>
               </v-row>
             </v-container>
             <v-expansion-panel-content>
               <template v-for="val, key in dependencies">
                 <template v-if="val.init && showInit">
                   <div style="color: green;" v-katex="val.name + ' = ' + val.init" :key="'init_'+key"></div>
                 </template>
                 <template v-for="math, i  in val.math">
                   <div 
                    v-katex="math" :key="'math_'+key+i"></div>
                   <v-divider light :key="'div_'+key+i"></v-divider>
                 </template>
               </template>
             </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </div>
    
    <v-tooltip right v-if="!math">
      <template #activator="{ on }">
        <v-chip v-on="on" small 
        v-if="url">
          <a :href="url" target="_blank">
            {{ text }}
            <v-icon small> mdi-open-in-new</v-icon>
          </a>
        </v-chip>
        <v-chip 
          v-on="on" 
          small 
          @click="copyToClipBoard(text)" 
          v-else-if="text"
          >
            {{ text }}
            <v-icon small class="ml-2"> mdi-content-copy</v-icon>
        </v-chip>
      </template>
      <span>{{tooltip}}</span>
    </v-tooltip>
    
  </div>
  
</template>

<script>
  export default {
    name: 'pmr-chips',
    props: {
      'url':{ //url, text, math
        type: String,
        default:null,
      }, 
      'text':{
        type: String,
        default:null,
      }, 
      'math':{
        type: String,
        default:null,
      },
      'dependencies':{
        type: Object,
        default:null,
      },
      'componentCode':{
        type: String,
        default:null,
      },
      'tooltip':{
        type: String,
        default:'Open external url',
      },
    },
    methods: {
      copyToClipBoard(textToCopy){
        if (typeof textToCopy === 'string' || textToCopy instanceof String)
          navigator.clipboard.writeText(textToCopy);
        else{
          let result = ""
          for (const k in textToCopy){
            if (textToCopy[k].init)
              result += textToCopy[k].name + ' = ' + textToCopy[k].init + " \\\\ "
            for (const k2 in textToCopy[k].math)
              result += textToCopy[k].math[k2] + " \\\\ "
          }
          navigator.clipboard.writeText(result);
        }
      },
    },
    data() {
      return {
        showInit:false,
        fab: false,
      }
    }
  }
</script>

<style>
  .v-speed-dial {
    position: absolute;
  }
  .v-btn--floating {
    position: relative;
  }
  .katex { font-size: 1.1em; }
</style>