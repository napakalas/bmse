<template>
  <v-app id="bmse">
    <v-navigation-drawer
      v-model="drawer"
      app
      width="350"
    >
      <v-row
        align="center"
        justify="center"
        class="mt-6 mb-6"
      >
        <v-list
          dense
          nav
        >
          <v-list-item>
            <v-list-item-content>
              <v-img src="Logo-BMSE.png" max-height="150" max-width="150"></v-img>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-row>

        <!-- <v-list
          dense
          nav
        >
          <v-list-item
            v-for="item in items"
            :key="item.title"
            :to="item.to"
            link
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list> -->
        <v-card
          class="mx-auto"
          max-width="400"
          v-if="varIds.length > 0"
        >
          <v-toolbar
            flat
            color="grey darken-3"
            dark
          >
            <v-toolbar-title>Entity Types</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-chip-group
              v-model="entityTypeSelected"
              column
              multiple
            >
              <v-chip
                v-for="entityType in entityTypes"
                :key="entityType"
                :value="entityType"
                filter
                outlined
                small
                >
                {{entityType}}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>    
        
        <v-card
          class="mx-auto"
          max-width="400"
          v-if="varIds.length > 0"
        >
          <v-toolbar
            flat
            color="grey darken-3"
            dark
          >
            <v-toolbar-title>Filter</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-switch
              v-model="isAnd"
              label="AND"
              class="mt-2"
              @change="setFilter(varIds, varSelectedFilters, varFilters, 'variable')"
            />
          </v-toolbar>

          <v-card-text v-if="getSelectedEntityTypes.includes('variable')">
            <h2 class="text-h6 mb-2">
              Variable
            </h2>
            <v-chip-group
              v-model="varSelectedFilters"
              column
              multiple
              @change="setFilter(varIds, varSelectedFilters, varFilters, 'variable')"
            >
              <v-chip
                v-for="(value, key) in varFilters"
                :key="key"
                :value="key"
                filter
                outlined
                small
                >
                {{key}}:{{value.name}}
              </v-chip>
            </v-chip-group>
          </v-card-text>
          
          <v-card-text v-if="getSelectedEntityTypes.includes('component')">
            <h2 class="text-h6 mb-2">
              Component
            </h2>
            <v-chip-group
              v-model="compSelectedFilters"
              column
              multiple
              @change="setFilter(compIds, compSelectedFilters, compFilters, 'component')"
            >
              <v-chip
                v-for="(value, key) in compFilters"
                :key="key"
                :value="key"
                filter
                outlined
                small
                >
                {{key}}:{{value.name}}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-navigation-drawer>
    <!-- <v-app-bar
      app
      color="#fcb69f"
      dark
      src="dna.jpg"
      :height="varIds.length > 0?50:190"
    > -->
    <v-app-bar
      app
      color="white"
      :height="varIds.length > 0?50:190"
    >
      <!-- <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(19,84,122,.5), rgba(128,208,199,.8)"
        ></v-img>
      </template> -->
      <v-app-bar-nav-icon @click="drawer = !drawer" v-if="varIds.length > 0"></v-app-bar-nav-icon>
      <v-spacer></v-spacer>
      <v-img class="mr-6" src="Logo-BMSE.png" max-height="150" max-width="150" v-if="varIds.length === 0"></v-img>
      <v-toolbar-title class="text mr-6"><b class="titleStyle">Biosimulation Model Search Engine</b></v-toolbar-title>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <router-view  
        :getParentData="getParentData" 
        :selectedEntityTypes="getSelectedEntityTypes"
        :compSelected="compSelected"
        >
      </router-view>
    </v-main>
  </v-app>
</template>

<script>
  import { EventBus } from './event-bus';
  export default {
    computed: {
      getParentData() {
        return this.varSelected;
      },
      getSelectedEntityTypes() {
        if (this.entityTypeSelected.length === 0)
          return this.entityTypes
        else
          return this.entityTypeSelected
      },
    },
    data: () => ({
      drawer: false,
      items: [
          { title: 'Todo', icon: 'mdi-format-list-checks', to: '/'},
          { title: 'About', icon: 'mdi-help-box', to: '/about'},
        ],
        
      isAnd: true,
      // variable filter
      varFilters: {},
      varIds: [],
      varSelectedFilters:[],
      varSelected: [],
      
      // component filter
      compFilters: {},
      compIds: [],
      compSelectedFilters: [],
      compSelected: [],
      
      // for entity types selection
      entityTypes: ['variable', 'component', 'CellML', 'SEDML', 'image'],
      entityTypeSelected: [],
    }),
    mounted() {
      EventBus.$on("passEntityFilters", data  => {
        this.varFilters = data['filters']; // data to filter appearance from child
        this.varIds = data['entities']; // list of entitiID
        this.varSelectedFilters = []; // classIds selected using v-chip
        this.varSelected = data['entities']; // list of presented entityID
        this.drawer = true
      }),
      EventBus.$on("passComponentFilters", data  => {
        this.compFilters = data['filters']
        this.compIds = data['entities']
        this.compSelectedFilters = []
        this.compSelected = data['entities']
      }),
      document.title = "BMSE | Biosimulasion Model Search Engine (PMR)";
    },
    methods: {
      setFilter(entityList, selectedFilters, filters, type){
        let classArray = entityList;
        if (selectedFilters.length > 0){
          if (this.isAnd){
            for (const classId of selectedFilters){
              classArray = classArray.filter(value => filters[classId]["entities"].includes(value));
            }
          } else {
            if (selectedFilters !== 0)
              classArray = []
            for (const classId of selectedFilters){
              classArray = classArray.concat(filters[classId]["entities"]);
            }
          }
        }
        if (type==='variable')
          this.varSelected = classArray
        else if (type==='component')
          this.compSelected = classArray
      },
    },
  };

</script>

<style>
.titleStyle {
  font-size: 2rem !important;
}
</style>