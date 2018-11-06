var dropdowns = {
  personas: {
    'Summer': ['All', 'Germany'],
    'Post-summer': ['All', 'United States']
  },
  trajectories: {
    'Pre-summer': ['Germany', 'United States', 'China'],
    'Summer': ['Germany', 'Netherlands', 'France'],
    'Post-summer': ['Germany', 'United States'],
    'Winter': ['China']
  }
}

var dictionaryObj = {
  locations: [
    { season: "Summer", 
      value: "locations/Location_cluster_summer.html", 
      description: "In this plot we can see an example of the results we can obtain by using this clustering methodology. In this case we are looking at the results for the summer period (June to August 2017) for all nationalities. What emerges from this graph are some patterns of visits, such as the fact that Pisa and Florence are visited together and so are Livorno and the islands. We can also see that the coast is not visited in its entirety in summer but it’s split in northern, middle, and southern parts of the municipalities." },
    { season: "Post-summer", 
      value: "locations/Location_cluster_post_summer.html", 
      description: "In this plot we can see how the summer behaviour persists in the post-summer season with some small changes. We see that Pisa and Livorno are still visited together, and that the coast is still split in north, middle and southern parts. However, we see that Livorno is not grouped with islands anymore and the centre of the region is more homogeneous." },
    { season: "Winter",
      value: "locations/Location_cluster_winter.html", 
      description: "Immediately from the the winter cluster we see that clusters are more homogeneous. Municipalities in the northern, central and the southern parts of the region are clamped together. Florence and Pisa are not in the same cluster anymore. This results in a reduction of the number of bigger clusters, a possible indication that tourists travel less during winter season." }
  ],
  personas: [
    {
      season: "Summer",
      country: "Germany",
      value: "personas/personas_germany_summer.html",
      description: "<p>During last year’s summer season (Jun-Aug)  roughly <0.5> million tourists from Germany   visited Tuscany. The data shows us 3 distinct types of behaviours for tourists from Germany.</p><p> <p>First, we have those who stay in the region for an average duration of 6 days; these tourists typically spend at least half a day on the coast and half a day in Florence.</p> <p>A second group of tourists seem to be spending on average a total of 9 days in the region, and at least half a day in Livorno, Florence, Pisa, and Lucca</p>.<p> Third, we have those who spend 13 days, and visit for at least half a day Florence, Lucca, Pisa, Grosseto, and Siena.</p>"
    },
    {
      season: "Post-summer",
      country: "United States",
      value: "personas/personas_united states_post_summer.html",
      description: "<p>During last year’s post-summer season (Sep-Oct) roughly 0.2 million tourists from the USA. The data shows us 4 distinct types of behaviours for tourists from the USA</p>. <p>First, we have the <i>countrysiders</i> who stay in the region for an average duration of 4 days; these tourists typically spend at least half a day in Florence.</p> <p>A second group of tourists, the <i>exlporers</i> seem to be spending on average a total of 7 days in the region, and at least half a day in Florence and Siena.</p> <p>Third, we have the <i>cruisers</i> who spend 15 days, and visit for at least half a day on the coast and in Livorno, and Pisa.</p> <p> Lastly, we have the <i>city hoppers</i> who spend 4 days in the region, and at least half a day in Florence</p>"
    },
    {
      season: "Summer",
      country: "All",
      value: "personas/personas_all_summer.html",
      description: "<p>During last year’s summer season (Jun-Aug) roughly 3 million tourists visited Tuscany. The majority of these tourists were coming from Germany (16.3%),  France (10.3%) United Kingdom (9.1%), United States (8.6%), and The Netherlands (8.2%). The data shows us 4 distinct types of behaviours for tourists (of all nationalities).</p><p>First type of behaviour, the <i>city hopper</i>, is followed by almost half of the people (45%), who spend on average 4 days in Tuscany, during which at least half a day is in Florence. Out of all nationalities, those who fall in this bucket are: United States (12%), Germany (11.9%), United Kingdom (9%), France (7.5%), and Netherlands (7.4%).</p><p>ourists in the second largest type of behaviour, the <i>coast lover</i>, covering 34% of all visitors, spend on average 6 days in Tuscany. During their holidays they spend at least half a day on the coast and half a day in the coast, Pisa, Livorno, Lucca, and Florence. Out of all nationalities, those who fall in this bucket are: Germany (21.2%), France (13%),  United Kingdom (9.8%), Netherlands (8.7%), and Switzerland (7.3%).</p><p> Tourists in the third largest type of behaviour, the <i>explorer</i>, covering 12.7% of all visitors, spend on average 11 days in Tuscany. During their holidays they spend at least half a day on the coast and half a day in Florence, the coast, Pisa, Siena, and Lucca. Out of all nationalities, those who fall in this bucket are: Germany (19.9%), France (12.5%), Netherlands (10.9%), United States (7.2%), and United Kingdom (6.7%).</p><p> Tourists in the fourth largest type of behaviour, the <i>countrysider</i>, covering 7.8% of all visitors, spend on average 9 days in Tuscany. During their holidays they spend at least half a day in Florence. Out of all nationalities, those who fall in this bucket are: Germany (17.4%), France (14.5%), Switzerland (7.9%), United States (6.5%), and Netherlands (5.7%).</p>"
    },
    {
      season: "Post-summer",
      country: "All",
      value: "personas/personas_all_post_summer.html",
      description: "<p>During last year’s post-summer season (Sep-Oct) roughly 1.5 million tourists visited Tuscany. The majority of these tourists were coming from Germany (15.2%), United States (13.6%), United Kingdom (8.5%), France (6.9%), and the Netherlands (6.5%). The data shows us 4 distinct types of behaviours for tourists (of all nationalities).</p><p>First type of behaviour, the <i>city hopper</i>, is followed by almost half of the people (49.2%), who spend on average 3 days in Tuscany, during which at least half a day is in Florence. Out of all nationalities, those who fall in this bucket are: United States (17.7%), Germany (10.8%), United Kingdom (7.8%), China (6.9%), and France (6.1%).</p> <p> Tourists in the second largest type of behaviour, the <i>coast lover</i>, covering 29.6% of all visitors, spend on average 5 days in Tuscany. During their holidays they spend at least half a day on the coast and half a day in the coast, Livorno, Pisa, Florence, and Lucca. Out of all nationalities, those who fall in this bucket are: Germany (21.5%), Switzerland (10.8%), United Kingdom (9.8%), France (9.7%), and United States (8.7%).</p><p> Tourists in the third largest type of behaviour, the <i>explorer</i>, covering 10.8% of all visitors, spend on average 8 days in Tuscany. During their holidays they spend at least half a day on the coast and half a day in Florence, the coast, Pisa, and Siena. Out of all nationalities, those who fall in this bucket are: Germany (19.3%), United States (14.1%), United Kingdom (7.8%), Spain (6.8%), and Netherlands (6.2%).</p><p> Tourists in the fourth largest type of behaviour, the <i>countrysider</i>, covering 10.4% of all visitors, spend on average 5 days in Tuscany. During their holidays they spend at least half a day in Florence. Out of all nationalities, those who fall in this bucket are: Germany (15%), China (9.5%), United States (9%), France (6.8%), and Netherlands (6.8%)</p>"
    }
    ],
  trajectories: [
    {
      season: "Pre-summer",
      country: "Germany",
      cluster: "Summary",
      value: "germany_pre_summer/Germany_pre-summer_summary.html",
      description: "<p>In the last pre-summer season (May 2017), the data shows us 3 clusters. Each line in the graph above represents a cluster's typical path that tourists from Germany followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Exploring Tuscan countryside, spends on average 6.4 days in Italy, 6.1 of which in Tuscany. When in Tuscany, Exploring Tuscan countryside spend at least a half day in The Coast, Florence, and Livorno. The second cluster, which we named Central Tuscany Trips, spends on average 6.4 days in Italy, 6.1 of which in Tuscany. When in Tuscany, Central Tuscany Trips spend at least a half day in The Coast, Florence, and Livorno. The third cluster, which we named Coastal Trips, spends on average 6.3 days in Italy, 6.0 of which in Tuscany. When in Tuscany, Coastal Trips spend at least a half day in The Coast, and Florence. </p>"},
    {
      season: "Pre-summer",
      country: "Germany",
      cluster: "Coastal trips",
      value: ["germany_pre_summer/Germany_pre-summer_coastal_trips_heatmap.html"
      ,"germany_pre_summer/Germany_pre-summer_coastal_trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Coastal Trips</i> cluster. The darker the colour, the more Coastal Trips visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (6.0% of the tourists in this cluster). The next most visited municipalities are San Gimignano (4.0%), and Pisa (4.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Coastal Trips cluster."
    },
    {
      season: "Pre-summer",
      country: "Germany",
      cluster: "Central Tuscany trips",
      value: ["germany_pre_summer/Germany_pre-summer_central_tuscany_trips_heatmap.html",
        "germany_pre_summer/Germany_pre-summer_central_tuscany_trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Central Tuscany Trips</i> cluster. The darker the colour, the more Central Tuscany Trips visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (44.0% of the tourists in this cluster). The next most visited municipalities are San Gimignano (37.0%), and Poggibonsi (30.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Central Tuscany Trips cluster."
    },
    {
      season: "Pre-summer",
      country: "Germany",
      cluster: "Exploring Tuscany countryside",
      value: ["germany_pre_summer/Germany_pre-summer_exploring_Tuscany_countryside_heatmap.html",
        "germany_pre_summer/Germany_pre-summer_exploring_Tuscany_countryside.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Exploring Tuscan countryside</i> cluster. The darker the colour, the more Exploring Tuscan countryside visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (62.0% of the tourists in this cluster). The next most visited municipalities are San Gimignano (53.0%), and Poggibonsi (44.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Exploring Tuscan countryside cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Summary",
      value: "germany_summer/Germany_summer_summary.html",
      description: "<p>In the last summer season (Jun - Aug 2017), the data shows us 6 clusters. Each line in the graph above represents a cluster's typical path that tourists from Germany followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Around Cecina, spends on average 11.8 days in Italy, 11.6 of which in Tuscany. When in Tuscany, Around Cecina spend at least a half day in The Coast, and Livorno. The second cluster, which we named Short Tuscany Trips (Florence and one other), spends on average 5.3 days in Italy, 5.0 of which in Tuscany. When in Tuscany, Short Tuscany Trips (Florence and one other) spend at least a half day in The Coast, and Florence. The third cluster, which we named Trips to Elba, spends on average 13.1 days in Italy, 12.9 of which in Tuscany. When in Tuscany, Trips to Elba spend at least a half day in The Coast, and Livorno. The forth cluster, which we named Around Florence, spends on average 10.7 days in Italy, 10.5 of which in Tuscany. When in Tuscany, Around Florence spend at least a half day in Florence, The Coast, Pisa, Siena, Lucca, and Livorno. The fifth cluster, which we named Stay at Grosseto, spends on average 12.6 days in Italy, 12.4 of which in Tuscany. When in Tuscany, Stay at Grosseto spend at least a half day in The Coast, Grosseto, and Florence. The sixth cluster, which we named To Livorno, spends on average 17.8 days in Italy, 17.5 of which in Tuscany. When in Tuscany, To Livorno spend at least a half day in The Coast, Livorno, Pisa, Lucca, Florence, and Arezzo. </p>"
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Around Cecina",
      value: ["germany_summer/Germany_summer_around_cecina_heatmap.html",
        "Germany_summer_around_cecina.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Around Cecina</i> cluster. The darker the colour, the more Around Cecina visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Cecina (61.0% of the tourists in this cluster). The next most visited municipalities are Castagneto Carducci (45.0%), and Bibbona (42.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Around Cecina cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Around Florence",
      value: ["germany_summer/Germany_summer_around_florence_heatmap.html",
        "germany_summer/Germany_summer_around_florence.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Around Florence</i> cluster. The darker the colour, the more Around Florence visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited San Gimignano (53.0% of the tourists in this cluster). The next most visited municipalities are Gambassi Terme (47.0%), and Poggibonsi (42.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Around Florence cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Short Tuscany trips",
      value: ["germany_summer/Germany_summer_short_tuscany_trips_heatmap.html",
        "germany_summer/Germany_summer_short_tuscany_trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Short Tuscany Trips (Florence and one other)</i> cluster. The darker the colour, the more Short Tuscany Trips (Florence and one other) visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (36.0% of the tourists in this cluster). The next most visited municipalities are Reggello (31.0%), and Viareggio (27.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Short Tuscany Trips (Florence and one other) cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Stay at Grosseto",
      value: ["germany_summer/Germany_summer_stay_at_Grosseto_heatmap.html",
        "germany_summer/Germany_summer_stay_at_Grosseto.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Stay at Grosseto</i> cluster. The darker the colour, the more Stay at Grosseto visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Grosseto (36.0% of the tourists in this cluster). The next most visited municipalities are Grosseto (36.0%), and Grosseto (36.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Stay at Grosseto cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Livorno lovers",
      value: ["germany_summer/Germany_summer_to_Livorno_heatmap.html",
        "germany_summer/Germany_summer_to_Livorno.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>To Livorno</i> cluster. The darker the colour, the more To Livorno visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Livorno (13.0% of the tourists in this cluster). The next most visited municipalities are Livorno (13.0%), and Livorno (13.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the To Livorno cluster."
    },
    {
      season: "Summer",
      country: "Germany",
      cluster: "Trips to Elba",
      value: ["germany_summer/Germany_summer_trips_to_elba_heatmap.html",
        "germany_summer/Germany_summer_trips_to_elba.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Trips to Elba</i> cluster. The darker the colour, the more Trips to Elba visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Capoliveri (43.0% of the tourists in this cluster). The next most visited municipalities are Capoliveri (43.0%), and Capoliveri (43.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Trips to Elba cluster."
    },
    {
      season: "Post-summer",
      country: "Germany",
      cluster: "Summary",
      value: "germany_post_summer/Germany_post-summer_summary.html",
      description: "<p>In the last post-summer season (Sep - Nov, 2017), the data shows us 5 clusters. Each line in the graph above represents a cluster's typical path that tourists from Germany followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Around Florence, spends on average 2.0 days in Italy, 1.8 of which in Tuscany. When in Tuscany, Around Florence spend at least a half day in Florence, and The Coast. The second cluster, which we named Florence and Rome, spends on average 7.0 days in Italy, 6.6 of which in Tuscany. When in Tuscany, Florence and Rome spend at least a half day in The Coast, and Florence. The third cluster, which we named Tuscany Trips, spends on average 8.1 days in Italy, 7.8 of which in Tuscany. When in Tuscany, Tuscany Trips spend at least a half day in The Coast, Florence, Siena, and Lucca. The forth cluster, which we named Coastal trips, spends on average 15.1 days in Italy, 14.8 of which in Tuscany. When in Tuscany, Coastal trips spend at least a half day in Livorno, The Coast, and Pisa. The fifth cluster, which we named Trips to Elba, spends on average 11.2 days in Italy, 11.0 of which in Tuscany. When in Tuscany, Trips to Elba spend at least a half day in The Coast, and Livorno. </p>"
    },
    {
      season: "Post-summer",
      country: "Germany",
      cluster: "Around Florence",
      value: ["germany_post_summer/Germany_post-summer_Around_Florence.html",
        "germany_post_summer/Germany_post-summer_Around_Florence_heatmap.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Around Florence</i> cluster. The darker the colour, the more Around Florence visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (24.0% of the tourists in this cluster). The next most visited municipalities are Pisa (19.0%), and Livorno (14.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Around Florence cluster."
    },
     {
      season: "Post-summer",
      country: "Germany",
      cluster: "Coastal Trips",
      value: ["germany_post_summer/Germany_post-summer_CoastalTrips_heatmap.html",
        "germany_post_summer/Germany_post-summer_CoastalTrips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Coastal trips</i> cluster. The darker the colour, the more Coastal trips visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Livorno (11.0% of the tourists in this cluster). The next most visited municipalities are Livorno (11.0%), and Livorno (11.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Coastal trips cluster."
    },
     {
      season: "Post-summer",
      country: "Germany",
      cluster: "Florence and Rome",
      value: ["germany_post_summer/Germany_post-summer_FlorenceandRome_heatmap.html",
        "germany_post_summer/Germany_post-summer_FlorenceandRome.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and Rome</i> cluster. The darker the colour, the more Florence and Rome visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (9.0% of the tourists in this cluster). The next most visited municipalities are Calenzano (7.0%), and Civitella in Val di Chiana (6.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and Rome cluster."
    },
     {
      season: "Post-summer",
      country: "Germany",
      cluster: "Trips to Elba",
      value: ["germany_post_summer/Germany_post-summer_Trips_to_Elba_heatmap.html",
        "germany_post_summer/Germany_post-summer_Trips_to_Elba.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Trips to Elba</i> cluster. The darker the colour, the more Trips to Elba visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Capoliveri (32.0% of the tourists in this cluster). The next most visited municipalities are Capoliveri (32.0%), and Capoliveri (32.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Trips to Elba cluster."
    },
    {
      season: "Post-summer",
      country: "Germany",
      cluster: "Tuscany Trips",
      value: ["germany_post_summer/Germany_post-summer_TuscanyTrips_heatmap.html",
        "germany_post_summer/Germany_post-summer_TuscanyTrips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Tuscany Trips</i> cluster. The darker the colour, the more Tuscany Trips visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited San Gimignano (93.0% of the tourists in this cluster). The next most visited municipalities are Firenze (89.0%), and Poggibonsi (70.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Tuscany Trips cluster."
    },
    {
      season: "Pre-summer",
      country: "United States",
      cluster: "Summary",
      value: "us_pre_summer/United States_pre-summer_summary.html",
      description: "<p>In the last pre-summer season (May 2017), the data shows us 3 clusters. Each line in the graph above represents a cluster's typical path that tourists from United States followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Central Italy Trips, spends on average 5.8 days in Italy, 5.5 of which in Tuscany. When in Tuscany, Central Italy Trips spend at least a half day in Florence, and Siena. The second cluster, which we named Mainly Florence, spends on average 5.7 days in Italy, 5.4 of which in Tuscany. When in Tuscany, Mainly Florence spend at least a half day in Florence, and Siena. The third cluster, which we named Big city lovers, spends on average 5.9 days in Italy, 5.6 of which in Tuscany. When in Tuscany, Big city lovers spend at least a half day in Florence, and Siena. </p> "
    },
    {
      season: "Pre-summer",
      country: "United States",
      cluster: "Central Italy Trip",
      value: ["us_pre_summer/United States_pre-summer_CentralItalyTrip_heatmap.html",
        "us_pre_summer/United States_pre-summer_CentralItalyTrip.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Central Italy Trips</i> cluster. The darker the colour, the more Central Italy Trips visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (95.0% of the tourists in this cluster). The next most visited municipalities are Cortona (37.0%), and Montepulciano (36.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Central Italy Trips cluster."
    },
      {
      season: "Pre-summer",
      country: "United States",
      cluster: "Big City Lovers",
      value: ["us_pre_summer/United States_pre-summer_BigCityLovers_heatmap.html",
        "us_pre_summer/United States_pre-summer_BigCityLovers.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Big city lovers</i> cluster. The darker the colour, the more Big city lovers visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (56.0% of the tourists in this cluster). The next most visited municipalities are Poggibonsi (21.0%), and Siena (21.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Big city lovers cluster."
    },
      {
      season: "Pre-summer",
      country: "United States",
      cluster: "Mainly Florence",
      value: ["us_pre_summer/United States_pre-summer_MainlyFlorence_heatmap.html",
        "us_pre_summer/United States_pre-summer_MainlyFlorence.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Mainly Florence</i> cluster. The darker the colour, the more Mainly Florence visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (66.0% of the tourists in this cluster). The next most visited municipalities are Montepulciano (25.0%), and Poggibonsi (24.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Mainly Florence cluster."
    },
    {
      season: "Post-summer",
      country: "United States",
      cluster: "Summary",
      value: "us_post_summer/United States_post-summer_summary.html",
      description: "<p>In the last post-summer season (Sep - Nov, 2017), the data shows us 4 clusters. Each line in the graph above represents a cluster's typical path that tourists from United States followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Florence and Cinque Terre, spends on average 5.3 days in Italy, 4.9 of which in Tuscany. When in Tuscany, Florence and Cinque Terre spend at least a half day in Florence, Livorno, The Coast, and Pisa. The second cluster, which we named Only Florence, spends on average 4.7 days in Italy, 4.5 of which in Tuscany. When in Tuscany, Only Florence spend at least a half day in Florence, and Siena. The third cluster, which we named Tuscany to Rome, spends on average 3.1 days in Italy, 2.7 of which in Tuscany. When in Tuscany, Tuscany to Rome spend at least a half day in Florence, Pisa, The Coast, and Livorno. The forth cluster, which we named Tuscany Explorers, spends on average 9.1 days in Italy, 8.7 of which in Tuscany. When in Tuscany, Tuscany Explorers spend at least a half day in Florence, and Siena. </p>"
    },
    {
      season: "Post-summer",
      country: "United States",
      cluster: "Florence & Cinque Terre",
      value: ["us_post_summer/United States_post-summer_Florence&CT_heatmap.html",
        "us_post_summer/United States_post-summer_Florence&CT.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and Cinque Terre</i> cluster. The darker the colour, the more Florence and Cinque Terre visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (73.0% of the tourists in this cluster). The next most visited municipalities are Poggibonsi (28.0%), and Montepulciano (28.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and Cinque Terre cluster."
    },
    {
      season: "Post-summer",
      country: "United States",
      cluster: "Only Florence",
      value: ["us_post_summer/United States_post-summer_OnlyFlorence_heatmap.html",
        "us_post_summer/United States_post-summer_OnlyFlorence.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Only Florence</i> cluster. The darker the colour, the more Only Florence visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (61.0% of the tourists in this cluster). The next most visited municipalities are Siena (25.0%), and Poggibonsi (24.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Only Florence cluster."
    },
    {
      season: "Post-summer",
      country: "United States",
      cluster: "Tuscany to Rome",
      value: ["us_post_summer/United States_post-summer_Tuscany_to_Rome_heatmap.html",
        "us_post_summer/United States_post-summer_Tuscany_to_Rome.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Tuscany to Rome</i> cluster. The darker the colour, the more Tuscany to Rome visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (17.0% of the tourists in this cluster). The next most visited municipalities are Pisa (17.0%), and Livorno (13.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Tuscany to Rome cluster."
    },
    {
      season: "Post-summer",
      country: "United States",
      cluster: "Tuscany Explorers",
      value: ["us_post_summer/United States_post-summer_TuscanyExplorers_heatmap.html",
        "us_post_summer/United States_post-summer_TuscanyExplorers.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Tuscany Explorers</i> cluster. The darker the colour, the more Tuscany Explorers visited that municipality during the post-summer season (Sep - Nov, 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (80.0% of the tourists in this cluster). The next most visited municipalities are Siena (47.0%), and Montepulciano (45.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Tuscany Explorers cluster."
    },
    {
      season: "Pre-summer",
      country: "China",
      cluster: "Summary",
      value: "china_pre_summer/china_pre_summer_summary.html",
      description: "<p>In the last pre-summer season (May 2017), the data shows us 2 clusters. Each line in the graph above represents a cluster's typical path that tourists from China followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Around Tuscany, spends on average 3.0 days in Italy, 2.5 of which in Tuscany. When in Tuscany, Around Tuscany spend at least a half day in Florence. The second cluster, which we named City Hoppers, spends on average 2.9 days in Italy, 2.4 of which in Tuscany. When in Tuscany, City Hoppers spend at least a half day in Florence. </p>"},
    {
      season: "Pre-summer",
      country: "China",
      cluster: "City Hoppers",
      value: ["china_pre_summer/China_pre-summer_clusterwise_trajectories_City_hoppers.html",
        "china_pre_summer/WEBSITE_China_pre-summer_City_Hoppers_heatmap.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>City Hoppers</i> cluster. The darker the colour, the more City Hoppers visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (41.0% of the tourists in this cluster). The next most visited municipalities are Rignano sull'Arno (27.0%), and Reggello (24.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the City Hoppers cluster."},
    {
      season: "Pre-summer",
      country: "China",
      cluster: "Around Tuscany",
      value: ["china_pre_summer/WEBSITE_China_pre-summer_Around_Tuscany_heatmap.html",
        "china_pre_summer/China_pre-summer_clusterwise_trajectories_Around_tuscany.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Around Tuscany</i> cluster. The darker the colour, the more Around Tuscany visited that municipality during the pre-summer season (May 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (160.0% of the tourists in this cluster). The next most visited municipalities are Rignano sull'Arno (105.0%), and Reggello (92.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Around Tuscany cluster."
    },
    {
      season: "Winter",
      country: "China",
      cluster: "Summary",
      value: "china_winter/China_winter_summary.html",
      description: "<p>In the last winter season (Dec 2017 - Feb 2018), the data shows us 3 clusters. Each line in the graph above represents a cluster's typical path that tourists from China followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Rome-Florence-Cinque Terre, spends on average 2.6 days in Italy, 2.1 of which in Tuscany. When in Tuscany, Rome-Florence-Cinque Terre spend at least a half day in Florence. The second cluster, which we named Major Italian Attractions, spends on average 2.6 days in Italy, 2.1 of which in Tuscany. When in Tuscany, Major Italian Attractions spend at least a half day in Florence. The third cluster, which we named Florence and North Italy trips, spends on average 2.6 days in Italy, 2.1 of which in Tuscany. When in Tuscany, Florence and North Italy trips spend at least a half day in Florence. </p>"
    },
    {
      season: "Winter",
      country: "China",
      cluster: "Major Italian Attractions",
      value: ["china_winter/China_winter_Major_Italian_Attractions_heatmap.html",
        "china_winter/China_winter_Major_Italian_Attractions.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Major Italian Attractions</i> cluster. The darker the colour, the more Major Italian Attractions visited that municipality during the winter season (Dec 2017 - Feb 2018). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (77.0% of the tourists in this cluster). The next most visited municipalities are Reggello (72.0%), and Rignano sull'Arno (72.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Major Italian Attractions cluster."
    },
    {
      season: "Winter",
      country: "China",
      cluster: "Florence and North Italy trips",
      value: ["china_winter/China_winter_Florence_and_North_Italy_trips_heatmap.html",
        "china_winter/China_winter_Florence_and_North_Italy_trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and North Italy trips</i> cluster. The darker the colour, the more Florence and North Italy trips visited that municipality during the winter season (Dec 2017 - Feb 2018). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (35.0% of the tourists in this cluster). The next most visited municipalities are Reggello (33.0%), and Rignano sull'Arno (32.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and North Italy trips cluster."
    },
    {
      season: "Winter",
      country: "China",
      cluster: "Rome Florence Cinque Terre",
      value: ["china_winter/China_winter_Rome-Florence-Cinque_Terre_heatmap.html",
        "china_winter/China_winter_Rome-Florence-Cinque_Terre.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Rome-Florence-Cinque Terre</i> cluster. The darker the colour, the more Rome-Florence-Cinque Terre visited that municipality during the winter season (Dec 2017 - Feb 2018). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (170.0% of the tourists in this cluster). The next most visited municipalities are Reggello (159.0%), and Rignano sull'Arno (158.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Rome-Florence-Cinque Terre cluster."
    },
    {
      season: "Summer",
      country: "Netherlands",
      cluster: "Summary",
      value: "netherlands_summer/Netherlands_summer_summary.html",
      description: "<p>In the last summer season (Jun - Aug 2017), the data shows us 4 clusters. Each line in the graph above represents a cluster's typical path that tourists from Netherlands followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Tuscany Trips, spends on average 13.2 days in Italy, 12.9 of which in Tuscany. When in Tuscany, Tuscany Trips spend at least a half day in Florence, The Coast, Lucca, Pisa, and Siena. The second cluster, which we named Around Florence, spends on average 6.4 days in Italy, 6.1 of which in Tuscany. When in Tuscany, Around Florence spend at least a half day in The Coast, Florence, and Pisa. The third cluster, which we named Central Coast Trips, spends on average 13.4 days in Italy, 13.1 of which in Tuscany. When in Tuscany, Central Coast Trips spend at least a half day in The Coast, and Florence. The forth cluster, which we named Countrysiders, spends on average 13.2 days in Italy, 12.9 of which in Tuscany. When in Tuscany, Countrysiders spend at least a half day in Siena, The Coast, Florence, Pisa, and Arezzo. <p>"
    },
    {
      season: "Summer",
      country: "Netherlands",
      cluster: "Around Florence",
      value: ["netherlands_summer/Netherlands_summer_Around_Florence_heatmap.html",
        "netherlands_summer/Netherlands_summer_Around_Florence.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Around Florence</i> cluster. The darker the colour, the more Around Florence visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited b'Firenze' (77.0% of the tourists in this cluster). The next most visited municipalities are b'Cortona' (70.0%), and b'San Gimignano' (47.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Around Florence cluster."
    },
    {
      season: "Summer",
      country: "Netherlands",
      cluster: "Central Coast Trips",
      value: ["netherlands_summer/Netherlands_summer_Central_Coast_Trips_heatmap.html",
        "netherlands_summer/Netherlands_summer_Central_Coast_Trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Central Coast Trips</i> cluster. The darker the colour, the more Central Coast Trips visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited b'Campiglia Marittima' (173.0% of the tourists in this cluster). The next most visited municipalities are b'Piombino' (113.0%), and b'Piombino' (113.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Central Coast Trips cluster."
    },
    {
      season: "Summer",
      country: "Netherlands",
      cluster: "Countrysiders",
      value: ["netherlands_summer/Netherlands_summer_Countrysiders_heatmap.html",
        "netherlands_summer/Netherlands_summer_Countrysiders.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Countrysiders</i> cluster. The darker the colour, the more Countrysiders visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Reggello (81.0% of the tourists in this cluster). The next most visited municipalities are Castelfranco Piandisco (44.0%), and Figline e Incisa Valdarno (58.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Countrysiders cluster."
    },
    {
      season: "Summer",
      country: "Netherlands",
      cluster: "Tuscany Trips",
      value: ["netherlands_summer/Netherlands_summer_Tuscany_Trips_heatmap.html",
        "netherlands_summer/Netherlands_summer_Tuscany_Trips.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Tuscany Trips</i> cluster. The darker the colour, the more Tuscany Trips visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Cecina (40.0% of the tourists in this cluster). The next most visited municipalities are Bibbona (95.0%), and Rosignano Marittimo (53.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Tuscany Trips cluster."
    },
    {
      season: "Summer",
      country: "France",
      cluster: "Summary",
      value: "france_summer/France_summer_summary.html",
      description: "<p>In the last summer season (Jun - Aug 2017), the data shows us 3 clusters. Each line in the graph above represents a cluster's typical path that tourists from France followed. These paths are displayed as differently-coloured lines in the map here above. The first cluster, which we named Florence and Rome, spends on average 3.1 days in Italy, 2.7 of which in Tuscany. When in Tuscany, Florence and Rome spend at least a half day in Florence. The second cluster, which we named Florence and Siena, spends on average 11.6 days in Italy, 11.3 of which in Tuscany. When in Tuscany, Florence and Siena spend at least a half day in Florence, Siena, The Coast, Pisa, and Lucca. The third cluster, which we named Florence and Pisa, spends on average 8.7 days in Italy, 8.5 of which in Tuscany. When in Tuscany, Florence and Pisa spend at least a half day in Florence, The Coast, Pisa, Lucca, and Livorno. </p>"
    },
    {
      season: "Summer",
      country: "France",
      cluster: "Florence and Pisa",
      value: ["france_summer/France_summer_clusterwise_heatmap_F&P.html",
        "france_summer/France_summer_clusterwise_trajectories_F&P.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and Pisa</i> cluster. The darker the colour, the more Florence and Pisa visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (76.0% of the tourists in this cluster). The next most visited municipalities are Pisa (61.0%), and San Gimignano (45.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and Pisa cluster."
    },
    {
      season: "Summer",
      country: "France",
      cluster: "Florence and Rome",
      value:["france_summer/France_summer_clusterwise_heatmap_F&R.html",
        "france_summer/France_summer_clusterwise_trajectories_F&R.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and Rome</i> cluster. The darker the colour, the more Florence and Rome visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited Firenze (18.0% of the tourists in this cluster). The next most visited municipalities are Pisa (13.0%), and Carrara (9.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and Rome cluster."
    },
    {
      season: "Summer",
      country: "France",
      cluster: "Florence and Siena",
      value:["france_summer/France_summer_clusterwise_heatmap_F&S.html",
        "france_summer/France_summer_clusterwise_trajectories_F&S.html"],
      description: "In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>Florence and Siena</i> cluster. The darker the colour, the more Florence and Siena visited that municipality during the summer season (Jun - Aug 2017). As we can see from the  heatmap, the majority of the tourists from  this cluster visited San Gimignano (66.0% of the tourists in this cluster). The next most visited municipalities are Firenze (65.0%), and Poggibonsi (55.0%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the Florence and Siena cluster."}]
};
