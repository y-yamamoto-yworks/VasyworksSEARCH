/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
 */
var { LMap, LTileLayer, LMarker, LIcon, LPopup } = Vue2Leaflet;

function createGarageSearchMapVue(
    key,    // キー
    zoom,   // ズーム
    lat,    // 緯度
    lng,    // 経度
) {
    return new Vue({
        el: "#contents",
        delimiters: ["[[", "]]"],
        components: {LMap, LTileLayer, LMarker, LIcon, LPopup},
        data: {
            conditionAreaIsHidden: true,
            maxDataCount: 100,
            message: "",
            key: key,       // APIデータ取得用
            zoom: 17,
            searchableMinZoom: 16,      // 検索可能な最小のズーム
            isSearchable: true,
            center: L.latLng(0, 0),
            default_lat: lat,
            default_lng: lng,
            url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            mapGarages: [],
            garages: [],
            mapLoading: false,
            lastBounds: null,
            iconOn: L.icon({
                iconUrl: "/static/search_map/images/car_icon_on.png",
                iconSize: [48, 48],
                iconAnchor: [24, 24],
            }),
            iconOff: L.icon({
                iconUrl: "/static/search_map/images/car_icon_off.png",
                iconSize: [48, 48],
                iconAnchor: [24, 24],
            }),
            lowerGarageFee: 0,
            upperGarageFee: 0,
            onlyOwn: false,
            forRent: false,
        },
        mounted: function(event) {
            // マウント後の処理
            this.center = L.latLng(this.default_lat, this.default_lng);
        },
        methods: {
            showConditions: function(event) {
                this.conditionAreaIsHidden = false;
            },
            hideConditions: function(event) {
                this.conditionAreaIsHidden = true;
            },
            submitConditions: function(event) {
                if(this.isSearchable && this.lastBounds) {
                    this.mapGarages = [];
                    this.searchGarages(this.lastBounds);
                }
            },
            clearConditions: function(event) {
                this.clearSubParams();
            },
            updateBounds: function(bounds) {
                // 地図の移動イベント
                this.lastBounds = null;
                if(this.isSearchable) {
                    this.lastBounds = bounds;
                    this.searchGarages(bounds);
                }
            },
            updateZoom: function(zoom) {
                // 地図のズームイベント
                if(zoom < this.searchableMinZoom) {
                    this.mapGarages = [];
                    this.garages = [];
                    this.isSearchable = false;
                } else {
                    this.isSearchable = true;
                }
            },
            mapMarkerClick: function(garage) {
                // マーカークリック済みの処理
                garage.icon = this.iconOff;
            },
            searchGarages: function(bounds) {
                // 地図検索
                if (this.mapGarages.length > 200) this.mapGarages = [];
                this.garages = [];

                north = bounds._northEast.lat;
                south = bounds._southWest.lat;
                east = bounds._northEast.lng;
                west = bounds._southWest.lng;

                if (north > 0 && south > 0 && east > 0 && west > 0) {
                    this.mapLoading = true;
                    let that = this;

                    // 緯度経度
                    let params = "north=" + north.toString();
                    params += "&south=" + south.toString();
                    params += "&east=" + east.toString();
                    params += "&west=" + west.toString();

                    let subParams = this.getSubParams();
                    if(subParams !== "") params += subParams;

                    let apiUrl = `/api/garages/${this.key}/?limit=${this.maxDataCount}&` + params
                    axios.get(apiUrl)
                        .then(function(res) {
                            that.message = ""
                            let items = res.data.list;
                            let dataCount = res.data.count;
                            if(dataCount > that.maxDataCount) {
                                that.message = `検索件数が上限の${that.maxDataCount}件を超えています。${that.maxDataCount}件以上は表示されません。`;
                            }
                            // 建物リスト
                            items.forEach( function(item) {
                                let lat = item.lat;
                                let lng = item.lng;

                                let icon = that.iconOn;
                                let mapImage = null;
                                let listImage = null;
                                if(item.garage_picture) {
                                    mapImage = item.garage_picture.thumbnail_file_url;
                                    listImage = item.garage_picture.medium_file_url
                                }
                                let garage = {
                                    id: item.id,
                                    linkId: item.oid,
                                    linkUrl: "/garage/" + item.oid,    // 要変更
                                    latLng: L.latLng(lat, lng),
                                    icon: icon,
                                    mapImage: mapImage,
                                    listImage: listImage,
                                    garageName: item.garage_name,
                                    address: item.address,
                                    garage_fee: item.garage_fee_text,
                                };

                                let isExists = false;
                                for(let i=0; i < that.mapGarages.length; i++) {
                                    if(that.mapGarages[i].id === garage.id) {
                                        isExists = true;
                                        break;
                                    }
                                }
                                if(!isExists) that.mapGarages.push(garage);
                                that.garages.push(garage);
                            });

                            that.mapLoading = false;
                        })
                        .catch(function (error) {
                            that.mapLoading = false;
                            alert("物件の取得に失敗しました。");
                        });
                }
            },
            getSubParams: function() {
                // 絞り込み条件パラメータ
                let ans = "";
                if(this.lowerGarageFee > 0) ans += "&l_fee=" + this.lowerGarageFee.toString();
                if(this.upperGarageFee > 0) ans += "&u_fee=" + this.upperGarageFee.toString();
                if(this.onlyOwn) ans += "&only_own=true";
                if(this.forRent) ans += "&for_rent=true";

                return ans;
            },
            clearSubParams: function() {
                this.lowerGarageFee = 0;
                this.upperGarageFee = 0;
                this.onlyOwn = false;
                this.forRent = false;
            },
        },
    });
}
