/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
 */
function createSearchBuildingIdVue(
    searchedBuildingId,
) {
    return Vue.createApp({
        delimiters: ["[[", "]]"],
        data() {
            return {
                building_id: searchedBuildingId,
            };
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.building_id = "";
            },
        },
    }).mount("#contents");
}
