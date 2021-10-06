/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
 */
function createSearchBuildingNameVue(
    searchedBuildingName,
) {
    return new Vue({
        el: "#contents",
        delimiters: ["[[", "]]"],
        data: {
            building_name: searchedBuildingName,
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.building_name = "";
            },
        },
    });
}
