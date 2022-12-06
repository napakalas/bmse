Tutorials
=========

Simple entity search
--------------------

Searching using BMSE is intuitive, as is the use of most commercial search 
engines. For example, we are looking for the mathematical equation for the 
concentration of glyceraldehyde-3-phosphate (GAP) in Astrocytes. Queries can 
use the term directly and do not need to worry about misspellings because BMSE 
considers the context of other syllables in the query. A synonym can also be 
used, for example, using `triose phosphate` instead of 
`glyceraldehyde-3-phosphate`. A good query requires the completeness of the 
terms needed to find the desired information. Here are the search steps:

1. Open website: https://search.bm-se.cloud.edu.au/

  .. image:: img/1.png
    :width: 600
    :alt: Text box to type a query in BMSE.

2. Type query, for example `concentration of triose phosphate in astrocyte`, 
   then press Enter. Here, we use `triose phosphate`, a synonym for 
   `glyceraldehyde-3-phosphate`.

  .. image:: img/2.png
    :width: 800
    :alt: The results of `concentration of triose phosphate in astrocyte` query.
  
  The search results are divided into two parts, on the left are filters to 
  restrict results, and on the right are query results for all types of 
  entities, i.e. variables, components, CellML, SEDML, and images.
  
.. raw:: latex

  \newpage
        
3. Since we are interested in a mathematical equation, the appropriate entity 
   is a `variable` or `component`. Suppose we are more interested in variables; 
   the view can be filtered by `variable`.
  
  .. image:: img/3.png
    :width: 600
    :alt: Showing the variable entity only.

4. Moreover, the list can be filtered further based on the ontology class, 
   which will limit the presented variables.

  .. image:: img/4.png
    :width: 600
    :alt: Variables filtered by ontology classes.
  
  In this case, we get one variable that best matches our search for a 
  mathematical equation.
  
5. Expanding the variable may be helpful to find out the associated images, 
   ontology classes, workspaces, CellML files, or exposures.
    
  .. image:: img/5.png
    :width: 600
    :alt: The expansion of a variable.
    
  In addition, we can find out the model of that variable. In this case, the 
  model relates to brain energy by :cite:t:`cloutier_integrative_2009`.
  
.. raw:: latex

  \newpage
          
6. A more detailed variable description is obtained by selecting the variable 
   and pressing the `Detail/Compare` button.
    
  .. image:: img/6.png
    :width: 600
    :alt: The more detail information of a variable
    
7. Furthermore, it can be followed by further activities, such as viewing 
   reference equations and copying them to latex and CellML formats.

  .. image:: img/7.png
    :width: 600
    :alt: The followed activities to show related mathematical equations.
    
.. raw:: latex

  \newpage
              
Variabel comparison
-------------------

A search with a less specific query, say `sodium channel voltage`, will return 
variables from several models. Even though the mathematical equations of these 
variables are similar, the initial values and other supporting equations can 
differ. These differences are related to different species or different 
experimental designs. BMSE facilitates variable comparison by presenting detail 
information regarding the selected vatiables

1. Here is the results of `sodium channel voltage` query:

  .. image:: img/8.png
    :width: 600
    :alt: The results of `sodium channel voltage` query.

2. Filtering the results using ontology classes does not always reduce the 
   choice, for example, when all variables are annotated similarly. Then, 
   the selection can be made by paying attention to the variable type, name, 
   initial value and mathematical equation.
   
 .. image:: img/9.png
   :width: 600
   :alt: Filtering by ontology classes is not always worked.

3. Another step is to sort, for example, by name to get variables with the same 
   name, type, unit, and mathematical equation differing in initial values.

 .. image:: img/10.png
   :width: 600
   :alt: The results after sorting by name.
   
4. After sorting, some variables can be expanded, 
   for example: :math:`fast\_sodium\_current/E_{Na}`.

  .. image:: img/11.png
    :width: 600
    :alt: The results after expanded.
    
5. Or compared

  .. image:: img/12.png
    :width: 600
    :alt: Action to compare variables.
  
  .. raw:: latex

    \newpage
      
  Example of a comparison display of 4 variables:
  
  .. image:: img/13.png
    :width: 600
    :alt: Variable comparison results.
  
  Some sections that may be helpful for comparison:
  
  Mathematical equation dependencies:
  
  .. image:: img/14.png
    :width: 600
    :alt: Mathematical equation dependencies.
    
  .. raw:: latex

    \newpage
      
  Source models, workspaces, exposures, and articles:
  
  .. image:: img/15.png
    :width: 600
    :alt: Source models, workspaces, exposures, and source articles.
  
  :cite:t:`faber_action_2000` :cite:t:`viswanathan_effects_1999` :cite:t:`winslow_mechanisms_1999`
  
  Comparing these sections is very helpful for selecting the 
  :math:`fast\_sodium\_current/E_{Na}` variable, for example, the one using 
  Guinea Pig :cite:p:`faber_action_2000, viswanathan_effects_1999` or 
  Canine Tachycardia-Induced Heart Failure :cite:p:`winslow_mechanisms_1999` 
  as experimental animals. 
  
..
  Other entity search (Component, CellML, SED-ML, and Image)
  ----------------------------------------------------------



