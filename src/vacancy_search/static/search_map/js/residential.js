/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
 */

function createResidentialSearchMapVue(
    key,    // キー
    zoom,   // ズーム
    lat,    // 緯度
    lng,    // 経度
) {
    if (key) {
        axios.defaults.headers.common['X-Api-Key'] = key;
    }

    return Vue.createApp({
        delimiters: ["[[", "]]"],
        data() {
            return {
                conditionAreaIsHidden: true,
                maxDataCount: 100,
                message: "",
                key: key,       // APIデータ取得用
                zoom: 17,
                searchableMinZoom: 16,      // 検索可能な最小のズーム
                isSearchable: true,
                default_lat: lat,
                default_lng: lng,
                url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
                attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
                mapBuildings: [],
                buildings: [],
                lastBounds: null,
                iconOn: L.icon({
                    iconUrl: "/static/search_map/images/building_icon_on.png",
                    iconSize: [48, 48],
                    iconAnchor: [24, 24],
                }),
                iconOff: L.icon({
                    iconUrl: "/static/search_map/images/building_icon_off.png",
                    iconSize: [48, 48],
                    iconAnchor: [24, 24],
                }),
                buildingTypes: [10, 20, 21, 30, 31, 40, 50, 51, 90],
                buildingAge: 0,
                withGarage: false,
                withBikeParking: false,
                layoutCategories: [10, 20, 30, 40, 50],
                lowerRent: 30000,
                upperRent: 0,
                includeCondoFees: false,
                lowerRoomArea: 0,
                upperRoomArea: 0,
                directions: [1, 2, 3, 4, 5, 6, 7, 8],
                roomFloor: 0,
                topFloor: false,
                separate: false,
                gasKitchen: false,
                freeInternet: false,
                indoorWasher: false,
                aircon: false,
                washstand: false,
                washingToilet: false,
                deliveryBox: false,
                autoLock: false,
                elevator: false,
                pet: false,
                instrument: false,
                liveTogether: false,
                roomShare: false,
                newStudent: false,
                nonJapanese: false,
                officeUse: false,
                onlyOwn: false,
                forRent: true,
                map: null,
                markerGroup: null,
                markersMap: {},
                mapLoading: null,
            };
        },
        mounted: function(event) {
            // マウント後の処理
            this.$nextTick(function() {
                this.initMap();
            });
        },
        methods: {
            initMap: function() {
                var mapEl = document.getElementById('id_map');
                if (!mapEl) return;

                this.map = L.map('id_map', {
                    scrollWheelZoom: false,
                    preferCanvas: true
                }).setView([this.default_lat, this.default_lng], this.zoom);

                L.tileLayer(this.url, {
                    attribution: this.attribution
                }).addTo(this.map);

                this.mapLoading = L.control({ position: 'topleft' });
                this.mapLoading.onAdd = function(map) {
                    var divLoading = L.DomUtil.create('div', 'map-loading');
                    divLoading.innerHTML = 'Loading...';
                    divLoading.style.display = 'none';

                    divLoading.style.fontSize = '24px';
                    divLoading.style.fontWeight = 'bold';
                    divLoading.style.color = '#dddddd';
                    divLoading.style.backgroundColor = '#999999';
                    divLoading.style.padding = '15px 30px';
                    divLoading.style.borderRadius = '8px';
                    divLoading.style.boxShadow = '0 4px 15px rgba(0,0,0,0.5)';

                    divLoading.style.position = 'fixed';
                    divLoading.style.top = '50%';
                    divLoading.style.left = '50%';
                    divLoading.style.transform = 'translate(-50%, -50%)';
                    divLoading.style.zIndex = '9999';

                    return divLoading;
                };
                this.mapLoading.addTo(this['map']);

                this.markerGroup = L.layerGroup().addTo(this.map);

                this.map.on('moveend zoomend', () => {
                    let currentZoom = this.map.getZoom();
                    this.updateZoom(currentZoom);

                    if (this.isSearchable) {
                        let bounds = this.map.getBounds();
                        this.updateBounds(bounds);
                    }
                });

                let initialBounds = this.map.getBounds();
                this.updateBounds(initialBounds);
            },
            showConditions: function(event) {
                this.conditionAreaIsHidden = false;
            },
            hideConditions: function(event) {
                this.conditionAreaIsHidden = true;
            },
            submitConditions: function(event) {
                if(this.isSearchable && this.lastBounds) {
                    this.clearAllMarkers();
                    this.searchBuildings(this.lastBounds);
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
                    this.searchBuildings(bounds);
                }
            },
            updateZoom: function(zoom) {
                // 地図のズームイベント
                if(zoom < this.searchableMinZoom) {
                    this.clearAllMarkers();
                    this.buildings = [];
                    this.isSearchable = false;
                } else {
                    this.isSearchable = true;
                }
            },
            clearAllMarkers: function() {
                this.mapBuildings = [];
                if (this.markerGroup) {
                    this.markerGroup.clearLayers();
                }
                this.markersMap = {};
            },
            searchBuildings: function(bounds) {
                // 地図検索
                if (this.mapBuildings.length > 200) this.clearAllMarkers();
                this.buildings = [];

                let north = bounds._northEast.lat;
                let south = bounds._southWest.lat;
                let east = bounds._northEast.lng;
                let west = bounds._southWest.lng;

                if (north > 0 && south > 0 && east > 0 && west > 0) {
                    if (this.mapLoading && this.mapLoading.getContainer()) {
                        this.mapLoading.getContainer().style.display = 'block';
                    }

                    let that = this;

                    // 緯度経度
                    let params = "north=" + north.toString();
                    params += "&south=" + south.toString();
                    params += "&east=" + east.toString();
                    params += "&west=" + west.toString();

                    let subParams = this.getSubParams();
                    if(subParams !== "") params += subParams;

                    let apiUrl = `/api/residential_buildings/?limit=${this.maxDataCount}&` + params
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
                                if(item.exterior_picture) {
                                    mapImage = item.exterior_picture.thumbnail_file_url;
                                    listImage = item.exterior_picture.medium_file_url
                                }
                                let building = {
                                    id: item.id,
                                    linkId: item.oid,
                                    linkUrl: "/building/" + item.oid,    // 要変更
                                    latLng: L.latLng(lat, lng),
                                    icon: icon,
                                    mapImage: mapImage,
                                    listImage: listImage,
                                    buildingName: item.building_name,
                                    address: item.address,
                                    rent: item.rent,
                                    layout: item.layout,
                                    build_year_month: item.build_year_month,
                                    building_type: item.building_type_text,
                                    structure: item.structure_text,
                                    building_floors: item.building_floors,
                                    building_rooms: item.building_rooms,
                                    bike_parking_type: item.bike_parking_type_text,
                                    garage_type: item.garage_type_text,
                                };

                                let isExists = false;
                                for(let i=0; i < that.mapBuildings.length; i++) {
                                    if(that.mapBuildings[i].id === building.id) {
                                        isExists = true;
                                        break;
                                    }
                                }
                                if(!isExists)
                                {
                                    that.mapBuildings.push(building);
                                    that.addBuildingMarker(building);
                                }
                                that.buildings.push(building);
                            });

                            if (that.mapLoading && that.mapLoading.getContainer()) {
                                that.mapLoading.getContainer().style.display = 'none';
                            }
                        })
                        .catch(function (error) {
                            if (that.mapLoading && that.mapLoading.getContainer()) {
                                that.mapLoading.getContainer().style.display = 'none';
                            }
                            alert("物件の取得に失敗しました。");
                        });
                }
            },
            addBuildingMarker: function(building) {
                if (!this['map'] || !this.markerGroup) return;
                if (this.markersMap[building.id]) return;

                let marker = L.marker(building.latLng, { icon: building.icon });

                let popupContent = this.createPopupContent(building);
                marker.bindPopup(popupContent);

                marker.on('click', () => {
                    building.icon = this.iconOff;
                    marker.setIcon(this.iconOff);
                });

                marker.addTo(this.markerGroup);
                this.markersMap[building.id] = marker;
            },
            createPopupContent: function(building) {
                let imageHtml = building.mapImage
                    ? `<img src="${building.mapImage}" class="img-fluid" alt="写真">`
                    : `<div class="no-image">No Image</div>`;

                return `
                    <table class="popup">
                        <tbody>
                            <tr>
                                <td colspan="2" class="building-name">
                                    <a href="${building.linkUrl}" target="_blank" rel="noopener noreferrer">${building.buildingName}</a>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" class="building-address">${building.address || ''}</td>
                            </tr>
                            <tr>
                                <td rowspan="8" class="building-image">
                                    <a href="${building.linkUrl}" target="_blank" rel="noopener noreferrer">
                                        ${imageHtml}
                                    </a>
                                </td>
                            </tr>
                            <tr><td class="building-item">【賃料】${building.rent || ''}</td></tr>
                            <tr><td class="building-item">【間取り】${building.layout || ''}</td></tr>
                            <tr><td class="building-item">${building.building_type || ''} ${building.building_floors || ''}階建</td></tr>
                            <tr><td class="building-item">${building.build_year_month || ''} 総戸数:${building.building_rooms || ''}戸</td></tr>
                            <tr><td class="building-item">${building.structure || ''}</td></tr>
                            <tr><td class="building-item">駐車場:${building.garage_type || ''}</td></tr>
                            <tr><td class="building-item">駐輪場:${building.bike_parking_type || ''}</td></tr>
                        </tbody>
                    </table>
                `;
            },
            getSubParams: function() {
                // 絞り込み条件パラメータ
                let ans = "";
                if(this.buildingTypes.length > 0) ans += "&b_tp=" + this.buildingTypes.join(',');
                if(this.buildingAge > 0) ans += "&b_age=" + this.buildingAge.toString();
                if(this.withGarage) ans += "&grg=true";
                if(this.withBikeParking) ans += "&bike=true";
                if(this.layoutCategories.length > 0) ans += "&lay=" + this.layoutCategories.join(',');
                if(this.lowerRent > 0) ans += "&l_rnt=" + this.lowerRent.toString();
                if(this.upperRent > 0) ans += "&u_rnt=" + this.upperRent.toString();
                if(this.includeCondoFees) ans += "&in_cnd=true";
                if(this.lowerRoomArea > 0) ans += "&l_ra=" + this.lowerRoomArea.toString();
                if(this.upperRoomArea > 0) ans += "&u_ra=" + this.upperRoomArea.toString();
                if(this.directions.length > 0 && this.directions.length < 8) ans += "&dir=" + this.directions.join(',');
                if(this.roomFloor === 1) ans += "&1_flr=true";
                if(this.roomFloor === 2) ans += "&2_flr=true";
                if(this.topFloor) ans += "&t_flr=true";
                if(this.separate) ans += "&sep=true";
                if(this.gasKitchen) ans += "&g_kn=true";
                if(this.freeInternet) ans += "&net_fr=true";
                if(this.indoorWasher) ans += "&in_wsh=true";
                if(this.aircon) ans += "&air=true";
                if(this.washstand) ans += "&wshstd=true";
                if(this.washingToilet) ans += "&wsh_wc=true";
                if(this.deliveryBox) ans += "&dlvr=true";
                if(this.autoLock) ans += "&a_lck=true";
                if(this.elevator) ans += "&elv=true";
                if(this.pet) ans += "&pet=true";
                if(this.instrument) ans += "&inst=true";
                if(this.liveTogether) ans += "&live_2=true";
                if(this.roomShare) ans += "&r_shr=true";
                if(this.newStudent) ans += "&new_std=true";
                if(this.nonJapanese) ans += "&no_jp=true";
                if(this.officeUse) ans += "&offc=true";
                if(this.onlyOwn) ans += "&only_own=true";
                if(this.forRent) ans += "&for_rent=true";

                return ans;
            },
            clearSubParams: function() {
                this.buildingTypes = [10, 20, 21, 30, 31, 40, 50, 51, 90];
                this.buildingAge = 0;
                this.withGarage = false;
                this.withBikeParking = false;
                this.layoutCategories = [10, 20, 30, 40, 50];
                this.lowerRent = 30000;
                this.upperRent = 0;
                this.includeCondoFees = false;
                this.lowerRoomArea = 0;
                this.upperRoomArea = 0;
                this.directions = [1, 2, 3, 4, 5, 6, 7, 8];
                this.roomFloor = 0;
                this.topFloor = false;
                this.separate = false;
                this.gasKitchen = false;
                this.freeInternet = false;
                this.indoorWasher = false;
                this.aircon = false;
                this.washstand = false;
                this.washingToilet = false;
                this.deliveryBox = false;
                this.autoLock = false;
                this.elevator = false;
                this.pet = false;
                this.instrument = false;
                this.liveTogether = false;
                this.roomShare = false;
                this.newStudent = false;
                this.nonJapanese = false;
                this.officeUse = false;
                this.onlyOwn = false;
                this.forRent = true;
            },
        },
    }).mount("#contents");
}
