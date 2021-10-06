/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
 */
function createSearchBuildingIdVue(
    searchedBuildingId,
) {
    return new Vue({
        el: "#contents",
        delimiters: ["[[", "]]"],
        data: {
            building_id: searchedBuildingId,
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.building_id = "";
            },
        },
    });
}
