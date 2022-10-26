<template>
  <v-row justify="center">
    <v-col
      cols="12"

    >
        <div class="pa-0">
          <v-chip-group
            active-class="primary--text"
            column
          >
            <pmr-chips 
              v-for="tag in getLeaves"
              :key="tag.name"
              :url="tag.url"
              :text="tag.name"
              :tooltip="tag.url?'Open external url':'Copy'"
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
    name: 'component-leaves',
    props: ['leaves'],
    components: {
      'pmr-chips': PMRChips,
    },
    data () {
      return {
        ontoUrl: {
          'FMA': 'https://bioportal.bioontology.org/ontologies/FMA/?p=classes&conceptid=http%3A%2F%2Fpurl.org%2Fsig%2Font%2Ffma%2FfmaCLASS_NUM#visualization',
          'CHEBI': 'https://bioportal.bioontology.org/ontologies/CHEBI/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FCHEBI_CLASS_NUM#visualization',
          'OPB': 'https://bioportal.bioontology.org/ontologies/OPB/?p=classes&conceptid=http%3A%2F%2Fbhi.washington.edu%2FOPB%23OPB_CLASS_NUM#visualization',
          'GO': 'https://bioportal.bioontology.org/ontologies/GO/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGO_CLASS_NUM#visualization',
          'UBERON': 'https://bioportal.bioontology.org/ontologies/UBERON/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FBFO_CLASS_NUM#visualization',
          'PR': 'https://www.ebi.ac.uk/ols/ontologies/pr/terms/graph?iri=http://purl.obolibrary.org/obo/PR_CLASS_NUM',
        },
      }
    },
    computed: {
      getLeaves() {
        let result = []
        
        
        for (const id in this.leaves){
          if (this.leaves[id].startsWith('http')){
            let classId = this.leaves[id].substring(this.leaves[id].lastIndexOf("/")+1)
            let ontology = classId.substring(0, classId.indexOf(":"));
            let classNum = classId.substring(classId.indexOf(":")+1);
            let url = this.ontoUrl[ontology].replace('CLASS_NUM', classNum)
            result.push({'name': classId, 'url': url})
          } else {
            result.push({'name': this.leaves[id]})
          }
        }
        return result
      }
    },
  }
</script>
<style>
  a { text-decoration: none; color: inherit;}
</style>