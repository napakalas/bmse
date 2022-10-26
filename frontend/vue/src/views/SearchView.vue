<template>
  <v-container fill-height fluid>
  
    <v-flex xs12 sm8 offset-sm2>
      <v-row 
        align="center"
        justify="center"
        >
        <v-col cols="12">
          <v-text-field
            v-model="query"
            label="Search by physiological terms"
            v-on:keyup.enter="search"
            clearable
            outlined
            type="text"
            prepend-inner-icon="mdi-magnify"
            ref="searchTextField"
          >
          </v-text-field>
        </v-col>
      </v-row>
    </v-flex>

    <v-col cols="12" v-if="selectedEntityTypes.includes('variable')">
      <v-data-table v-if="entities.length > 0"
          v-model="selectedCompare"
          :headers="entityHeaders"
          :items="dataVariables"
          :single-expand="singleExpand"
          item-key="id"
          show-expand
          show-select
          :item-selected="getMathDependencies()"
          class="elevation-1"
        > {{state}}
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Variable</v-toolbar-title>
            <comparison-page 
              :selectedCompare="selectedCompare" 
              :mathDependencies="mathDependencies"
              :componentCodes="varComponentCodes"
              v-if="selectedCompare.length > 0" 
            />
            <v-spacer></v-spacer>
            <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch>
          </v-toolbar>
        </template>
        
        <template v-slot:[`item.equation`]="{ item }">
          <template v-if="!item.math.length">
            -
          </template>
          <template v-else>
            <div 
              style="overflow-x: auto;overflow-y: hidden;white-space:nowrap;"
              v-katex="item.math[0]"></div>
          </template>
        </template>
        
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <v-card
              class="a-1 ma-1"
              max-width="entityHeaders.length"
              outlined color="transparent"
              >  
              <v-container fluid>
                <v-row 
                  dense
                  class="a-1 ma-1"
                  >
                  
                  <v-card
                    class="a-1 ma-1"
                    max-width="1000px"
                    outlined color="transparent"
                    v-if="carouselState[item.id]>-1"
                    > 
                    <carousel
                      :navigationEnabled="true"
                      :perPage="1"
                      :navigate-to="carouselState[item.id]"
                    >
                      <slide v-for="(image,i) in item.allImages"
                        :key="i"
                      >
                        <v-card
                          class="mx-auto"
                          outlined
                        >
                          <v-list-item>
                            <v-list-item-avatar
                              tile
                              height="50%"
                              width="auto"
                              color="#eeeeee"
                              >
                              <img :src="image.url"  :alt="image.url"/>
                            </v-list-item-avatar>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.title"
                              >
                              <div class="text-overline mb-4">
                                {{image.title}}
                              </div>
                            </v-list-item-content>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.variables"
                              >
                              <div 
                                v-for="variable, j in image.variables"
                                :key="j"
                                style="overflow-x: auto;overflow-y: hidden;white-space:nowrap;"
                                v-katex="variable.math[0] + '   (init=' + variable.init + ')'"
                                >
                              </div>
                            </v-list-item-content>
                          </v-list-item>
                          <v-card-actions>
                            <v-btn text icon absolute top right 
                              @click="carouselState[item.id]=-1; state=state+1;"
                            >
                              <v-icon>
                                mdi-close
                              </v-icon>
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </slide>
                    </carousel>
                  </v-card>
                  
                  <!-- Showing images as medium thumbnail -->
                  <template
                    v-if="carouselState[item.id]==-1"
                    >
                    <v-card  
                      hover
                      v-for="(image, i) in item.allImages"
                      :key="i"
                      class="ma-1"
                      width="300px"
                      >
                      <img 
                        :src="image.url"
                        height="auto"
                        width="290px"
                        class="ma-2"
                        @click="showCarousel(item.id, i);"  
                      > 
                    </v-card>
                  </template>
                  
                  <!-- Showing links for ontology classes -->
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.id]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Classes</v-toolbar-title>
                    </v-toolbar>
                    <classes-buttons 
                      :ontologyClasses="item.classes" 
                      :maxLength="35"
                      class="ma-2"
                    ></classes-buttons>
                  </v-card>
                  
                  <!-- Showing links for Cellml workspace, and exposure -->
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.id]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                      >
                      <v-toolbar-title>Sources</v-toolbar-title>
                    </v-toolbar>
                    <v-chip-group
                      active-class="primary--text"
                      column
                       class="pa-2 ma-2"
                      >
                      <pmr-chips 
                        :url="item.cellmlUrl"
                        :text="item.cellmlUrl.length > 35?'...'+item.cellmlUrl.substring(item.cellmlUrl.length-35):item.cellmlUrl"
                        :tooltip="'Open CellML'"
                      >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.workspaceUrl"
                        :text="item.workspaceUrl.length > 35?'...'+item.workspaceUrl.substring(item.workspaceUrl.length-35):item.workspaceUrl"
                        :tooltip="'Open workspace'"
                      >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.exposures[0]"
                        :text="item.exposures[0].length > 35?'...'+item.exposures[0].substring(item.exposures[0].length-35):item.exposures[0]"
                        :tooltip="'Open exposure'"
                        v-if="item.exposures.length > 0"
                      >
                      </pmr-chips>
                    </v-chip-group>
                  </v-card>
                  
                </v-row>
              </v-container>
            </v-card>
            
          </td>
        </template>
      </v-data-table>
    </v-col>

    <v-col cols="12" v-if="selectedEntityTypes.includes('component')">
      <v-data-table v-if="components.length > 0"
        :headers="componentHeaders"
        :items="dataComponents"
        :single-expand="singleExpand"
        item-key="id"
        show-expand
        class="elevation-1"
        @item-expanded="loadItemData"> 
        {{state}}
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Component</v-toolbar-title>
            <!-- <comparison-page 
              :selectedCompare="selectedCompare" 
              :mathDependencies="mathDependencies"
              v-if="selectedCompare.length > 0" 
            /> -->
            <v-spacer></v-spacer>
            <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch>
          </v-toolbar>
        </template>
        
        <template v-slot:[`item.equation`]="{ item }">
          <template v-if="!item.math.length">
            -
          </template>
          <template v-else>
            <div 
              style="overflow-x: auto;overflow-y: hidden;white-space:nowrap;"
              v-katex="item.math[0]"></div>
          </template>
        </template>
        
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <v-card
              class="a-1 ma-1"
              max-width="componentHeaders.length"
              outlined color="transparent"
              >  
              <v-container fluid>
                <v-row 
                  dense
                  class="a-1 ma-1"
                  >
                  
                  <!-- <v-card
                    class="a-1 ma-1"
                    max-width="80%"
                    outlined color="transparent"
                    v-if="carouselState[item.url]>-1"
                    > 
                    <carousel
                      :navigationEnabled="true"
                      :perPage="1"
                      :navigate-to="carouselState[item.url]"
                      >
                      <slide v-for="(image,i) in item.allImages"
                        :key="i"
                        >
                        <v-card
                          class="mx-auto"
                          max-width="80%"
                          outlined
                          >
                          <v-list-item>
                            <v-list-item-avatar
                              tile
                              height="auto"
                              width="70%"
                              color="#eeeeee"
                              >
                              <img :src="image.url"  :alt="image.url"/>
                            </v-list-item-avatar>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.title"
                              >
                              <div class="text-overline mb-4">
                                {{image.title}}
                              </div>
                            </v-list-item-content>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.variables"
                              >
                              <div 
                                v-for="variable, j in image.variables"
                                :key="j"
                                v-katex="variable.math[0] + '   (init=' + variable.init + ')'"
                                >
                              </div>
                            </v-list-item-content>
                          </v-list-item>
                          <v-card-actions>
                            <v-btn text icon absolute top right 
                              @click="carouselState[item.url]=-1; state=state+1;"
                            >
                              <v-icon>
                                mdi-close
                              </v-icon>
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </slide>
                    </carousel>
                  </v-card> -->
                  
                  <!-- <template
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-card  
                      hover
                      v-for="(image, i) in item.allImages"
                      :key="i"
                      class="ma-1"
                      width="300px"
                      >
                      <img 
                        :src="image.url"
                        height="auto"
                        width="290px"
                        class="ma-2"
                        @click="showCarousel(item.url, i);"  
                      > 
                    </v-card>
                  </template> -->
                  
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.id]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Classes</v-toolbar-title>
                    </v-toolbar>
                    <classes-buttons 
                      :ontologyClasses="item.classes" 
                      :maxLength="35"
                      class="ma-2"
                    ></classes-buttons>
                  </v-card>
                  
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.id]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Sources</v-toolbar-title>
                    </v-toolbar>
                    
                    <v-chip-group
                      active-class="primary--text"
                      column
                      class="pa-2 ma-2">
                      <pmr-chips 
                        :url="item.cellmlUrl"
                        :text="item.cellmlUrl.length > 35?'...'+item.cellmlUrl.substring(item.cellmlUrl.length-35):item.cellmlUrl"
                        :tooltip="'Open CellML'">
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.workspaceUrl"
                        :text="item.workspaceUrl.length > 35?'...'+item.workspaceUrl.substring(item.workspaceUrl.length-35):item.workspaceUrl"
                        :tooltip="'Open workspace'"
                      >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.exposures[0]"
                        :text="item.exposures[0].length > 35?'...'+item.exposures[0].substring(item.exposures[0].length-35):item.exposures[0]"
                        :tooltip="'Open exposure'"
                        v-if="item.exposures.length > 0"
                      >
                      </pmr-chips>
                    </v-chip-group>
                  </v-card>
                  <v-card
                    class="a-1 ma-1"
                    width="400px"
                    v-if="item.math.length > 0"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                      >
                      <v-toolbar-title>Maths</v-toolbar-title>    
                      <v-speed-dial
                        v-model="fab[item.id]"
                        :key="item.id"
                        :top="false"
                        :bottom="false"
                        :absolute="true"
                        :right="true"
                        :left="false"
                        :direction="'right'"
                        :open-on-hover="true"
                        :transition="'slide-y-transition'"
                        style="display: inline-block;"
                        >
                        <template v-slot:activator>
                          <v-btn
                            fab
                            color="white"
                            icon
                            x-small
                            >
                            <v-icon v-if="fab[item.id]">
                              mdi-close
                            </v-icon>
                            <v-icon v-else>
                              mdi-content-copy
                            </v-icon>
                          </v-btn>
                        </template>
                        <v-tooltip left color="green">
                          <template v-slot:activator="{ on }" >
                            <v-btn
                            fab
                            top
                            dark
                            x-small
                            color="green"
                            @click="copyToClipBoard(item.math)"
                            v-on="on"
                            >
                            CM
                            </v-btn>
                          </template>
                          <span>Copy math (LaTex)</span>
                        </v-tooltip>
                        <v-tooltip left color="red">
                          <template v-slot:activator="{ on }">
                            <v-btn
                              fab
                              top
                              dark
                              x-small
                              color="red"
                              @click="copyToClipBoard(item.componentCode)"
                              v-on="on"
                              >
                              CC
                            </v-btn>
                          </template>
                          <span>Copy CellML</span>
                        </v-tooltip>
                      </v-speed-dial>
                    </v-toolbar>
                    <div 
                      style="overflow-x: auto; overflow-y: auto;">
                      <div 
                        v-for="math in item.math"
                        :key="math"
                        v-katex="math"
                        class="pa-2 ma-2"
                        style="white-space:nowrap;"
                        >
                      </div>
                    </div>
                  </v-card>
                </v-row>
              </v-container>
            </v-card>
            
          </td>
        </template>
        
      </v-data-table>
    </v-col>
    
    <v-col cols="12" v-if="selectedEntityTypes.includes('CellML')">
      <v-data-table v-if="cellmls.length > 0"
          :headers="cellmlHeaders"
          :items="dataCellmls"
          :single-expand="singleExpand"
          item-key="url"
          show-expand
          class="elevation-1"
        > {{state}}
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>CellML</v-toolbar-title>
            <!-- <comparison-page 
              :selectedCompare="selectedCompare" 
              :mathDependencies="mathDependencies"
              v-if="selectedCompare.length > 0" 
            /> -->
            <v-spacer></v-spacer>
            <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch>
          </v-toolbar>
        </template>
        
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            
            <v-card
              class="a-1 ma-1"
              max-width="cellmlHeaders.length"
              outlined color="transparent"
              >  
              <v-container fluid>
                <v-row 
                  dense
                  class="a-1 ma-1"
                  >
                  
                  <v-card
                    class="a-1 ma-1"
                    max-width="80%"
                    outlined color="transparent"
                    v-if="carouselState[item.url]>-1"
                    > 
                    <carousel
                      :navigationEnabled="true"
                      :perPage="1"
                      :navigate-to="carouselState[item.url]"
                      >
                      <slide v-for="(image,i) in item.allImages"
                        :key="i"
                        >
                        <v-card
                          class="mx-auto"
                          max-width="80%"
                          outlined
                          >
                          <v-list-item>
                            <v-list-item-avatar
                              tile
                              height="auto"
                              width="70%"
                              color="#eeeeee"
                              >
                              <img :src="image.url"  :alt="image.url"/>
                            </v-list-item-avatar>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.title"
                              >
                              <div class="text-overline mb-4">
                                {{image.title}}
                              </div>
                            </v-list-item-content>
                            <v-list-item-content 
                              max-width="30%"
                              v-if="image.variables"
                              >
                              <div 
                                v-for="variable, j in image.variables"
                                :key="j"
                                style="overflow-x: auto;overflow-y: hidden;white-space:nowrap;"
                                v-katex="variable.math[0] + '   (init=' + variable.init + ')'"
                                >
                              </div>
                            </v-list-item-content>
                          </v-list-item>
                          <v-card-actions>
                            <v-btn text icon absolute top right 
                              @click="carouselState[item.url]=-1; state=state+1;"
                            >
                              <v-icon>
                                mdi-close
                              </v-icon>
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </slide>
                    </carousel>
                  </v-card>
                  
                  <template
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-card  
                      hover
                      v-for="(image, i) in item.allImages"
                      :key="i"
                      class="ma-1"
                      width="300px"
                      >
                      
                      <img 
                        :src="image.url"
                        height="auto"
                        width="290px"
                        class="ma-2"
                        @click="showCarousel(item.url, i);"  
                      > 
                    </v-card>
                  </template>
                  
                  <!-- <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Classes</v-toolbar-title>
                    </v-toolbar>
                    <classes-buttons 
                      :ontologyClasses="item.classes" 
                      :maxLength="35"
                      class="ma-2"
                    ></classes-buttons>
                  </v-card> -->
                  
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Sources</v-toolbar-title>
                    </v-toolbar>
                    
                    <v-chip-group
                      active-class="primary--text"
                      column
                       class="pa-2 ma-2"
                    >
                      <pmr-chips 
                        :url="item.url"
                        :text="item.url.length > 35?'...'+item.url.substring(item.url.length-35):item.url"
                        :tooltip="'Open CellML'"
                      >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.workspace"
                        :text="item.workspace.length > 35?'...'+item.workspace.substring(item.workspace.length-35):item.workspace"
                        :tooltip="'Open workspace'"
                      >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.exposure[0]"
                        :text="item.exposure[0].length > 35?'...'+item.exposure[0].substring(item.exposure[0].length-35):item.exposure[0]"
                        :tooltip="'Open exposure'"
                        v-if="item.exposure.length > 0"
                      >
                      </pmr-chips>
                    </v-chip-group>
                  </v-card>
                </v-row>
              </v-container>
            </v-card>
            
          </td>
        </template>
        
      </v-data-table>
    </v-col>
    
    <v-col cols="12" v-if="selectedEntityTypes.includes('SEDML')">
      <v-data-table v-if="sedmls.length > 0"
          :headers="sedmlHeaders"
          :items="dataSedmls"
          :single-expand="singleExpand"
          item-key="url"
          show-expand
          class="elevation-1"
        > {{state}}
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>SEDML</v-toolbar-title>
            <!-- <comparison-page 
              :selectedCompare="selectedCompare" 
              :mathDependencies="mathDependencies"
              v-if="selectedCompare.length > 0" 
            /> -->
            <v-spacer></v-spacer>
            <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch>
          </v-toolbar>
        </template>
        
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            
            <v-card
              class="a-1 ma-1"
              max-width="sedmlHeaders.length"
              outlined color="transparent"
              >  
              <v-container fluid>
                <v-row 
                  dense
                  class="a-1 ma-1"
                  >
                  
                  <v-card
                    class="a-1 ma-1"
                    max-width="1000px"
                    outlined color="transparent"
                    v-if="carouselState[item.url]>-1"
                    > 
                    <carousel
                      :navigationEnabled="true"
                      :perPage="1"
                      :navigate-to="carouselState[item.url]"
                      >
                      <slide v-for="(image,i) in item.plots"
                        :key="i"
                        >
                        <v-card
                          class="mx-auto"
                          outlined
                          >
                          <v-list-item>
                            <v-list-item-avatar
                              tile
                              width="550px"
                              height="auto"
                              color="#eeeeee"
                              >
                              <img :src="image.url"  :alt="image.url"/>
                            </v-list-item-avatar>
                            <v-list-item-content 
                              v-if="image.title"
                              >
                              <div class="text-overline mb-4">
                                {{image.title}}
                              </div>
                            </v-list-item-content>
                            <v-list-item-content 
                              v-if="image.variables"
                              >
                              <div 
                              v-for="variable, j in image.variables"
                              :key="j"
                              style="overflow-x: auto;overflow-y: hidden;white-space:nowrap;"
                              v-katex="variable.math[0] + '   (init=' + variable.init + ')'"
                                >
                              </div>
                            </v-list-item-content>
                          </v-list-item>
                          <v-card-actions>
                            <v-btn text icon absolute top right 
                              @click="carouselState[item.url]=-1; state=state+1;"
                              >
                              <v-icon>
                                mdi-close
                              </v-icon>
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </slide>
                    </carousel>
                  </v-card>
                  
                  <template
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-card  
                      hover
                      v-for="(image, i) in item.plots"
                      :key="i"
                      class="ma-1"
                      width="300px"
                      >
                      
                      <img 
                        :src="image.url"
                        height="auto"
                        width="290px"
                        class="ma-2"
                        @click="showCarousel(item.url, i);"  
                      > 
                    </v-card>
                  </template>
                  
                  <!-- <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Classes</v-toolbar-title>
                    </v-toolbar>
                    <classes-buttons 
                      :ontologyClasses="item.classes" 
                      :maxLength="35"
                      class="ma-2"
                    ></classes-buttons>
                  </v-card> -->
                  
                  <v-card  
                    class="a-1 ma-1"
                    width="300px"
                    v-if="carouselState[item.url]==-1"
                    >
                    <v-toolbar
                      color="indigo darken-4"
                      dark
                      dense
                      height="30px"
                    >
                      <v-toolbar-title>Sources</v-toolbar-title>
                    </v-toolbar>
                    
                    <v-chip-group
                      active-class="primary--text"
                      column
                       class="pa-2 ma-2"
                      >
                      <pmr-chips 
                        :url="item.url"
                        :text="item.url.length > 35?'...'+item.url.substring(item.url.length-35):item.url"
                        :tooltip="'Open SEDML'"
                        >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.cellmlUrl"
                        :text="item.cellmlUrl.length > 35?'...'+item.cellmlUrl.substring(item.cellmlUrl.length-35):item.cellmlUrl"
                        :tooltip="'Open CellML'"
                        >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.workspace"
                        :text="item.workspace.length > 35?'...'+item.workspace.substring(item.workspace.length-35):item.workspace"
                        :tooltip="'Open workspace'"
                        >
                      </pmr-chips>
                      <pmr-chips 
                        :url="item.exposure[0]"
                        :text="item.exposure[0].length > 35?'...'+item.exposure[0].substring(item.exposure[0].length-35):item.exposure[0]"
                        :tooltip="'Open exposure'"
                        v-if="item.exposure.length > 0"
                        >
                      </pmr-chips>
                    </v-chip-group>
                  </v-card>
                  
                </v-row>
              </v-container>
            </v-card>
            
          </td>
        </template>
        
      </v-data-table>
    </v-col>
    
    <v-col cols="12" align="center" v-if="selectedEntityTypes.includes('image')">
      <v-slide-group v-if="images.length > 0">
        <v-slide-item v-for="(image,i) in images" :key="i" class="ma-5">
          <v-card color="#eeeeee" elevation="10" max-width="300px" hover
            @click="selectedImage=i"
            >
            <v-img
              :src="image.url"
              height="200px"
            ></v-img>
            <v-card-text>
              {{image.caption.length > 200?image.caption.substring(0, 200)+' ...':image.caption}}
            </v-card-text>
          </v-card>
        </v-slide-item>
      </v-slide-group>
      <vue-gallery-slideshow :images="images" :index="selectedImage" color="#eeeeee" @close="selectedImage = null">dadsa<v-btn>test</v-btn></vue-gallery-slideshow>
      <!-- <v-dialog
        v-model="showImageGallery"
        max-width="1000px"
        max-height="600px"
        transition="dialog-bottom-transition"
         class="justify-center align-center"
        >
        <pmr-gallery></pmr-gallery>
      </v-dialog> -->
    </v-col>
    
  </v-container>
</template>

<script>

import PMRDataService from "../services/PMRDataService";
import { EventBus } from '@/event-bus';
import { Carousel, Slide } from 'vue-carousel';
import ComparisonPage from "../views/ComparisonPage"
import ClassesButtons from "../components/ClassesButtons"
import PMRChips from "../components/PMRChips"
// import VueGallerySlideshow from 'vue-gallery-slideshow'
import VueGallerySlideshow from '../components/PMRGallerySlideShow'

export default {
  name: "entity-search",
  props: {
      getParentData: {
        type: Array,
        required: true
      },
      selectedEntityTypes:{
        type: Array,
        required: true
      },
      compSelected:{
        type: Array,
        required: true
      },
    },
  watch: {
      getParentData(data) {
        this.selectedEntities = data;
      }
    },
  components: {
    'carousel': Carousel,
    'slide': Slide, 
    'comparison-page': ComparisonPage,
    'classes-buttons': ClassesButtons,
    'pmr-chips': PMRChips,
    'vue-gallery-slideshow': VueGallerySlideshow,
  },
  data() {
    return {
      // for entities / variables
      selectedCompare: [],
      mathDependencies: {},
      varComponentCodes: {},
      selectedEntities: [],
      query:"",
      singleExpand: false,
      entityHeaders: [
        { text: '', value: 'data-table-expand' },
        {
          text: 'Name',
          align: 'start',
          sortable: true,
          value: 'name',
        },
        { text: 'Init', value: 'init' },
        { text: 'Type', value: 'type' },
        { text: 'Unit', value: 'unit.name' },
        { text: 'Math', value: 'equation' },
      ],
      entities: [],

      //carousel
      carouselState:{},
      state: 0,
      
      // for cellmls
      cellmls: [],
      cellmlHeaders: [
        { text: '', value: 'data-table-expand' },
        { text: 'Title', value: 'title' },
        { text: 'File Name', value: 'fileName' },
        { text: 'Workspace', value: 'shortWks' },
        { text: 'SEDML', value: 'sortSedml' },
      ],
      
      // for sedmls
      sedmls: [],
      sedmlHeaders: [
        { text: '', value: 'data-table-expand' },
        { text: 'File Name', value: 'fileName' },
        { text: 'Workspace', value: 'shortWks' },
        { text: 'CellML Title', value: 'cellmlTitle' },
      ],
      plotPath: 'images/', //for deployment
      // plotPath: 'http://localhost:8000/images/', // for developments
      
      // for images
      images: [],
      showImageGallery:false,
      selectedImage: null,
      
      // for componentSearch
      components: [],
      componentHeaders: [
        { text: '', value: 'data-table-expand' },
        { text: 'Name', value: 'name' },
        { text: 'Workspace', value: 'shortWks' },
        { text: 'CellML', value: 'cellmlTitle' },
        { text: 'Math', value: 'equation' },
      ],
      
      fab: {},
    };
  },
  computed: {
    dataVariables() {
      let data = [];
      for (const pos in this.entities){
        if (this.selectedEntities.includes(this.entities[pos]['id'])){
          let tmp = this.entities[pos]
          tmp['allImages'] = tmp.cellmlImages.map((x) => x)
          for (const idx in tmp.sedmls){
            for (const i in tmp.sedmls[idx].plots)
              tmp.sedmls[idx].plots[i].url = this.plotPath + tmp.sedmls[idx].plots[i].url
            tmp['allImages'] = tmp['allImages'].concat(tmp.sedmls[idx].plots)
          }
          data.push(tmp);
        }
      }
      return data;
    },
    dataComponents() {
      let data = [];
      // console.log(this.components)
      for (const pos in this.components){
        if (this.compSelected.includes(this.components[pos]['id'])){
          let tmp = this.components[pos]
          let fileName = tmp.cellmlUrl.substring(tmp.cellmlUrl.lastIndexOf("HEAD/") + 5)
          tmp['cellml'] = this.splitLongSentence(fileName)
          let shortWks = tmp.workspaceUrl.substring(tmp.workspaceUrl.indexOf(".org") + 4)
          tmp['shortWks'] = this.splitLongSentence(shortWks)
          // tmp['allImages'] = tmp.plots.map((x) => x);
          data.push(tmp);
        }
      }
      return data
    },
    dataCellmls() {
      let data = [];
      for (const pos in this.cellmls){
        let tmp = this.cellmls[pos]
        let fileName = tmp.url.substring(tmp.url.lastIndexOf("HEAD/") + 5)
        tmp['fileName'] = this.splitLongSentence(fileName)
        let shortWks = tmp.workspace.substring(tmp.workspace.indexOf(".org") + 4)
        tmp['shortWks'] = this.splitLongSentence(shortWks)
        let shortSedml = tmp.sedmls.length === 0 ? '':tmp.sedmls[0].id.substring(tmp.sedmls[0].id.lastIndexOf("HEAD/") + 5)
        tmp['sortSedml'] = this.splitLongSentence(shortSedml)
        tmp['allImages'] = tmp.image.map((x) => x);
        for (const idx in tmp.sedmls){
          for (const i in tmp.sedmls[idx].plots)
            tmp.sedmls[idx].plots[i].url = this.plotPath + tmp.sedmls[idx].plots[i].url
          tmp['allImages'] = tmp['allImages'].concat(tmp.sedmls[idx].plots)
        }
        data.push(tmp);
      }
      return data;
    },
    dataSedmls() {
      let data = [];
      for (const pos in this.sedmls){
        let tmp = this.sedmls[pos]
        let fileName = tmp.url.substring(tmp.url.lastIndexOf("HEAD/") + 5)
        tmp['fileName'] = this.splitLongSentence(fileName)
        let shortWks = tmp.workspace.substring(tmp.workspace.indexOf(".org") + 4)
        tmp['shortWks'] = this.splitLongSentence(shortWks)
        tmp['allImages'] = tmp.plots;
        for (const i in tmp.allImages)
          tmp.allImages[i].url = this.plotPath + tmp.allImages[i].url;
        data.push(tmp);
      }
      return data;
    },
    
    
  },
  methods: {
    splitLongSentence(str){
      if (str.length <= 50)
        return str
      var regex = /_/gi, result, indices = [];
      while ( (result = regex.exec(str)) )
        indices.push(result.index);
      const pos = indices[Math.floor(indices.length/2)]
      let rs = str.substring(0,pos)+' '+str.substring(pos)
      return rs
    },
    search(){
      if (this.query.trim() != "")
        PMRDataService.entitySearch(this.query)
          .then((response) => {
            // initialising data needed
            this.entities = response.data.result;
            for (const i in this.entities){
              this.carouselState[this.entities[i]['id']] = -1;
            }
            this.selectedCompare = []
            this.mathDependencies = {}
            this.varComponentCodes = {}
            this.selectedEntities = []
            
            // set for parent view
            let filters =  response.data.filter;
            let arr = this.entities.map((v) => v.id);
            EventBus.$emit('passEntityFilters', {'filters':filters, 'entities':arr});
            
          })
          .catch((e) => {
            console.log(e);
          });
        
        PMRDataService.componentSearch(this.query)
          .then((response) => {
            this.components = response.data.result
            for (const i in this.components){
              this.carouselState[this.components[i]['id']] = -1;
            }
            // set for parent view
            let filters =  response.data.filter;
            let arr = this.components.map((v) => v.id);
            EventBus.$emit('passComponentFilters', {'filters':filters, 'entities':arr});
          })
          .catch((e) => {
            console.log(e);
          });
            
        PMRDataService.cellmlSearch(this.query)
          .then((response) => {
            this.cellmls = response.data;
            for (const i in this.cellmls){
              this.carouselState[this.cellmls[i]['url']] = -1;
            }
          })
          .catch((e) => {
            console.log(e);
          });
          
        PMRDataService.sedmlSearch(this.query)
          .then((response) => {
            this.sedmls = response.data;
            for (const i in this.sedmls){
              this.carouselState[this.sedmls[i]['url']] = -1;
            }
          })
          .catch((e) => {
            console.log(e);
          });
          
        PMRDataService.imageSearch(this.query)
          .then((response) => {
            this.images = response.data
          })
          .catch((e) => {
            console.log(e);
          });
          
    },
    showCarousel(objId, imgIndex){
      this.carouselState[objId]=imgIndex;
      this.state=this.state+1;
    },
    
    async getMathDependencies (){
      for (const selected in this.selectedCompare){
        const varId = this.selectedCompare[selected].id
        if (!Object.keys(this.mathDependencies).includes(varId)){
          PMRDataService.getMathDependencies(varId)
            .then((response) => {
              this.mathDependencies[varId] = response.data
            })
            .catch((e) => {
              console.log(e);
            });
          PMRDataService.getComponentCode(varId, 'variable')
            .then((response) => {
              this.varComponentCodes[varId] = response.data
            })
            .catch((e) => {
              console.log(e);
            });
        }
      }
    },
    loadItemData({item}){
      const type = item.id.startsWith("Var")?"variable":"component"
      PMRDataService.getMaths(item.id, type)
        .then((response) => {
          item.math = response.data
        })
        .catch((e) => {
          console.log(e);
        });
      PMRDataService.getComponentCode(item.id, type)
        .then((response) => {
          item.componentCode = response.data
        })
        .catch((e) => {
          console.log(e);
        });
        
    },
    copyToClipBoard(textToCopy){
      if (typeof textToCopy === 'string' || textToCopy instanceof String)
        navigator.clipboard.writeText(textToCopy);
      else{
        let result = ""
        for (const k in textToCopy){
            result += textToCopy[k] + " \\\\ "
        }
        navigator.clipboard.writeText(result);
      }
    },
  },
  mounted(){
    this.$nextTick(() => this.$refs.searchTextField.$refs.input.focus());
  },
};



</script>

<style>
.v-card__text, .v-card__title,  {
  word-break: normal; /* maybe !important  */
  width:250px;
  margin-left: 5px;
  margin-right: 5px;
}

.scrolling-box {
  background-color: #eaeaea;
  display: block;
  /* width: 100%; */
  /* height: 400px; */
  padding: 1em;
  overflow-y: scroll;
  text-align: center;
}
.vgs__container {
  background-color: #eaeaea !important; 
}
</style>
