/*
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
 */

function createGarageSearchMapVue(
    key,    // キー
    zoom,   // ズーム
    lat,    // 緯度
    lng,    // 経度
) {
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
                mapGarages: [],
                garages: [],
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
                    this.clearAllMarkers();
                    this.mapGarages = [];
                    this.garages = [];
                    this.isSearchable = false;
                } else {
                    this.isSearchable = true;
                }
            },
            clearAllMarkers: function() {
                this.mapGarages = [];
                if (this.markerGroup) {
                    this.markerGroup.clearLayers();
                }
                this.markersMap = {};
            },
            mapMarkerClick: function(garage) {
                // マーカークリック済みの処理
                garage.icon = this.iconOff;
            },
            searchGarages: function(bounds) {
                // 地図検索
                if (this.mapGarages.length > 200) this.mapGarages = [];
                this.garages = [];

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
                                if(!isExists)
                                {
                                    that.mapGarages.push(garage);
                                    that.addGarageMarker(garage);
                                }
                                that.garages.push(garage);
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
            addGarageMarker: function(garage) {
                if (!this['map'] || !this.markerGroup) return;
                if (this.markersMap[garage.id]) return;

                let marker = L.marker(garage.latLng, { icon: garage.icon });

                let popupContent = this.createPopupContent(garage);
                marker.bindPopup(popupContent);

                marker.on('click', () => {
                    garage.icon = this.iconOff;
                    marker.setIcon(this.iconOff);
                });

                marker.addTo(this.markerGroup);
                this.markersMap[garage.id] = marker;
            },
            createPopupContent: function(garage) {
                let imageHtml = garage.mapImage
                    ? `<img src="${garage.mapImage}" class="img-fluid" alt="写真">`
                    : `<div class="no-image">No Image</div>`;

                return `
                    <table class="popup">
                        <tbody>
                            <tr>
                                <td colspan="2" class="building-name">
                                    <a href="${garage.linkUrl}" target="_blank" rel="noopener noreferrer">${garage.garageName}</a>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" class="building-address">${garage.address || ''}</td>
                            </tr>
                            <tr>
                                <td rowspan="8" class="building-image">
                                    <a href="${garage.linkUrl}" target="_blank" rel="noopener noreferrer">
                                        ${imageHtml}
                                    </a>
                                </td>
                            </tr>
                            <tr><td class="building-item">【駐車料】${garage.garage_fee || ''}</td></tr>
                        </tbody>
                    </table>
                `;
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
    }).mount("#contents");
}
