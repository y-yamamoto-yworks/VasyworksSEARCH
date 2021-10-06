/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
 */
function createSearchBuildingCodeVue(
    searchedBuildingCode,
) {
    return new Vue({
        el: "#contents",
        delimiters: ["[[", "]]"],
        data: {
            building_code: searchedBuildingCode,
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.building_code = "";
            },
        },
    });
}
