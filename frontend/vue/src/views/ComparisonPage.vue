<template>
  
  <v-col cols="auto">
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          v-bind="attrs"
          v-on="on"
        >
          <v-icon dark>
            mdi-compare
          </v-icon>
          DETAIL/COMPARE
        </v-btn>
      </template>
      <template v-slot:default="dialog">
        <v-card>
          <v-container fluid>
            <v-data-iterator
              :items="selectedCompare"
              :items-per-page.sync="itemsPerPage"
              :page.sync="page"
              :search="search"
              :sort-by="sortBy.toLowerCase()"
              :sort-desc="sortDesc"
              hide-default-footer
            >
              <template v-slot:header>
                <v-toolbar
                  dark
                  color="blue darken-3"
                  class="mb-1"
                >
                  <v-text-field
                    v-model="search"
                    clearable
                    flat
                    solo-inverted
                    hide-details
                    prepend-inner-icon="mdi-magnify"
                    label="Search"
                  ></v-text-field>
                  <template v-if="$vuetify.breakpoint.mdAndUp">
                    <v-spacer></v-spacer>
                    <v-select
                      v-model="sortBy"
                      flat
                      solo-inverted
                      hide-details
                      :items="keys"
                      prepend-inner-icon="mdi-magnify"
                      label="Sort by"
                    ></v-select>
                    <v-spacer></v-spacer>
                    <v-btn-toggle
                      v-model="sortDesc"
                      mandatory
                    >
                      <v-btn
                        large
                        depressed
                        color="blue"
                        :value="false"
                      >
                        <v-icon>mdi-arrow-up</v-icon>
                      </v-btn>
                      <v-btn
                        large
                        depressed
                        color="blue"
                        :value="true"
                      >
                        <v-icon>mdi-arrow-down</v-icon>
                      </v-btn>
                    </v-btn-toggle>
                  </template>
                </v-toolbar>
              </template>

              <template v-slot:default="props">
                <v-row>
                  <v-col
                    v-for="item in props.items"
                    :key="item.id"
                    cols="12"
                    sm="6"
                    md="6"
                    lg="6"
                  >
                    <v-card>
                      <v-card-title class="subheading font-weight-bold">
                        {{ item.name }}
                      </v-card-title>

                      <v-divider></v-divider>

                      <v-list dense>
                        <v-list-item
                          v-for="(key, index) in filteredKeys"
                          :key="index"
                          class=" ma-0 "
                          >
                          <div class="text-overline ma-0 pa-0" style="width:20%"
                            v-if="key != 'allImages'"
                            >
                            <v-list-item-content 
                              :class="{ 'blue--text': sortBy === key }"
                              class="ma-0 pa-0"
                            >
                              {{ key
                                .replace(/([A-Z])/g, ' $1')
                                .replace(/^./, function(str){ return str.toUpperCase(); })
                              }}
                            </v-list-item-content>
                          </div>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-if="key==='id' || key==='name' || key==='init' || key==='type' || key === 'component'"
                          >
                            <component-leaves :leaves="[item[key].toString()]"></component-leaves>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'math'"
                          >
                            <template v-if="Object.keys(item.math).length > 0">
                                <pmr-chips
                                  :math="item.math[0]"
                                  :dependencies="mathDependencies[item.id]"
                                  :componentCode="componentCodes[item.id]"
                                  :tooltip="'Copy math'"
                                >
                                </pmr-chips>
                            </template>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'classes'"
                          >
                            <classes-buttons :ontologyClasses="item[key]"></classes-buttons>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'cellmlUrl'"
                          >
                            <cellml-buttons :cellmlUrls="[item[key]]" :type="'cellml'">
                            </cellml-buttons>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'workspaceUrl'"
                          >
                            <cellml-buttons :cellmlUrls="[item[key]]" :type="'workspace'">
                            </cellml-buttons>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'exposures'"
                          >
                            <cellml-buttons :cellmlUrls="item[key]" :type="'exposure'">
                            </cellml-buttons>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'similarCellmls'"
                          >
                            <cellml-buttons :cellmlUrls="item[key]" :type="'cellml'">
                            </cellml-buttons>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'compLeaves' || key === 'component'"
                          >
                            <component-leaves :leaves="item[key]"></component-leaves>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'sedmls'"
                          >
                            <!-- <cellml-buttons :cellmlUrls="$(item[key]).map(function() {return this.id;}).get()" :type="'cellml'"></cellml-buttons> -->
                            <sedml-images 
                              :sedmls="item[key]" 
                              :width="200">
                            </sedml-images>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'cellmlImages'"
                          >
                            <cellml-images 
                              :cellmlImages="item[key]" 
                              :width="200">
                            </cellml-images>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key === 'unit'"
                          >
                            <component-leaves :leaves="getUnit(item[key])"></component-leaves>
                          </v-list-item-content>
                          <v-list-item-content
                            class="align-end ma-0 pa-0"
                            :class="{ 'blue--text': sortBy === key }"
                            v-else-if="key !== 'math' && key != 'allImages'"
                          >
                            {{ item[key] }}
                          </v-list-item-content>
                          
                        </v-list-item>
                      </v-list>
                    </v-card>
                  </v-col>
                </v-row>
              </template>

              <template v-slot:footer>
                <v-row
                  class="mt-2"
                  align="center"
                  justify="center"
                >
                  <span class="grey--text">Items per page</span>
                  <v-menu offset-y>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        dark
                        text
                        color="primary"
                        class="ml-2"
                        v-bind="attrs"
                        v-on="on"
                      >
                        {{ itemsPerPage }}
                        <v-icon>mdi-chevron-down</v-icon>
                      </v-btn>
                    </template>
                    <v-list>
                      <v-list-item
                        v-for="(number, index) in itemsPerPageArray"
                        :key="index"
                        @click="updateItemsPerPage(number)"
                      >
                        <v-list-item-title>{{ number }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>

                  <v-spacer></v-spacer>
                  <span
                    class="mr-4
                    grey--text"
                  >
                    Page {{ page }} of {{ numberOfPages }}
                  </span>
                  <v-btn
                    fab
                    dark
                    color="blue darken-3"
                    class="mr-1"
                    @click="formerPage"
                  >
                    <v-icon>mdi-chevron-left</v-icon>
                  </v-btn>
                  <v-btn
                    fab
                    dark
                    color="blue darken-3"
                    class="ml-1"
                    @click="nextPage"
                  >
                    <v-icon>mdi-chevron-right</v-icon>
                  </v-btn>
                </v-row>
              </template>
            </v-data-iterator>
          </v-container>
          
          <v-card-actions class="justify-end">
            <v-btn
              text
              @click="dialog.value = false"
            >Close</v-btn>
          </v-card-actions>
          
        </v-card>
      </template>
    </v-dialog>
  </v-col>

</template>

<script>
  import ClassesButtons from "../components/ClassesButtons"
  import ComponentLeaves from "../components/ComponentLeaves"
  import CellmlImages from "../components/CellmlImages"
  import CellmlButtons from "../components/CellmlButtons"
  import SedmlImages from "../components/SedmlImages"
  import PMRChips from "../components/PMRChips"
  export default {
    name: 'comparison-page',
    props: ['selectedCompare', 'mathDependencies', 'componentCodes'],
    data () {
      return {
        itemsPerPageArray: [2,3,4],
        search: '',
        filter: {},
        sortDesc: false,
        page: 1,
        itemsPerPage: 2,
        sortBy: 'name',
        
        // for entity comparison purpose
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
      }
    },
    computed: {
      numberOfPages () {
        return Math.ceil(this.selectedCompare.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.keys.filter(key => key !== 'Name')
      },
      keys () {
        return Object.keys(this.selectedCompare[0])
      },
    },
    methods: {
      nextPage () {
        if (this.page + 1 <= this.numberOfPages) this.page += 1
      },
      formerPage () {
        if (this.page - 1 >= 1) this.page -= 1
      },
      updateItemsPerPage (number) {
        this.itemsPerPage = number
      },
      getUnit(unit){
        let result = []
        result.push(unit.name)
        return result
      },
    },
    components: {
      'classes-buttons': ClassesButtons,
      'component-leaves': ComponentLeaves,
      'cellml-images' : CellmlImages,
      'cellml-buttons' : CellmlButtons,
      'sedml-images': SedmlImages,
      'pmr-chips': PMRChips,
    }
    
  }
</script>