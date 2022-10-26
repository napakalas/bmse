<template>
  <v-row justify="center" class="pa-0 ma-0">
    <v-col
      cols="12"
       class="pa-0 ma-0"
    >
        <div class="pa-0 ma-0">
          <v-chip-group
            active-class="primary--text"
            column
             class="pa-0 ma-0"
          >
          <pmr-chips 
            v-for="url in shortCellmlUrl"
            :key="url.short"
            :url="url.url"
            :text="url.short.length > maxLength?'...'+url.short.substring(url.short.length-maxLength):url.short"
          >
          </pmr-chips>
          </v-chip-group>
        </div>
    </v-col>
  </v-row>
</template>

<script>
  import PMRChips from "../components/PMRChips"
  export default {
    name: 'cellml-buttons',
    props: {
      'cellmlUrls':{ 
        type: Array,
        default:null,
      }, 
      'type':{ //cellml, workspace, exposure
        type: String,
        default: null,
      },
      'maxLength':{ //maxLength
        type: Number,
        default: 1000,
      }
    },
    components: {
      'pmr-chips': PMRChips,
    },
    computed: {
      shortCellmlUrl (){
        let shortUrls = []
        for (const id in this.cellmlUrls){
          let start = "https://models.physiomeproject.org/workspace/".length
          let url = this.cellmlUrls[id]
          if (this.type === 'workspace'){ 
            shortUrls.push({'url':url, 'short':url.substring(start)})
          } else if (this.type === 'cellml') {
            let middle = url.indexOf('/rawfile')
            let tail = url.indexOf('HEAD/') + 5
            shortUrls.push({'url':url, 'short':url.substring(start, middle) + ':' + url.substr(tail)})  
          } else if (this.type === 'exposure'){
            start = "https://models.physiomeproject.org/".length
            shortUrls.push({'url':url, 'short':url.substring(start)})
          }
        }
        return shortUrls
      },
    },
  }
</script>