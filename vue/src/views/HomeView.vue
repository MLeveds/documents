<template>
    <header class="header">
        <span class="header__logo"><b>Documentos</b></span>
    </header>
    <div class="main">
        <div class="main__documents-list">
            <label for="upload-photo">
                <div
                    @drop.prevent="previewFile"
                    @dragenter.prevent="dragoverActive = true"
                    @dragover.prevent="dragoverActive = true"
                    @dragleave.prevent="dragoverActive = false"
                    class="main__documents-list__upload"
                >
                    <span v-if="!file">Нажмите для загрузки фото, или перетащите файл</span>
                    <template v-else>
                        <div class="upload_preview-image-container">
                            <img ref="preview-img" src="" alt="">
                        </div>
                        <div class="upload_preview-button-container">
                            <app-button @click="upload">
                                Загрузить
                            </app-button>
                        </div>
                    </template>
                </div>
            </label>
            <input @change="previewFile" type="file" name="photo" id="upload-photo" style="display:none;"/>

            <transition-group name="fade" mode="out-in">
                <div
                    @click="selectDocument(document)"
                    v-for="document in documents"
                    :key="document.id"
                    :style="selectedDocument && document.id === selectedDocument.id ? {'background-color': 'var(--purple)'} : {'background-color': 'var(--white)'}"
                    class="main__documents-list-item"
                >
                    <span style="width:5%; padding-left: 5%">{{ document['id'] }}</span>
                    <div style="width: 5%; padding-left: 5%">
                        <img style="max-height: 40px" :src="document['link']" alt="">
                    </div>
                    <span style="width:10%; padding-left: 20%">{{ document['status'] }}</span>
                    <span style="width: 30%; padding-left: 20%">{{ formatDate(document['created_at']) }}</span>
                </div>
            </transition-group>
        </div>
        <div class="main__documents-view">
            <template v-if="selectedDocument">
                <div class="main__documents-view__images">
                    <img class="main__documents-view__images__image" :src="selectedDocument['link']" alt="">
                    <img v-if="selectedDocument['edited_link']" class="main__documents-view__images__image" :src="selectedDocument['edited_link']" alt="">
                </div>
                <div class="main__documents-view__data">
                    <span><b>Статус: </b>{{ selectedDocument['status'] }}</span>
                    <span><b>Тип документа: </b>{{ selectedDocument['type'] ?? 'Не определен' }}</span>
                    <span><b>Страница: </b>{{ selectedDocument['page'] === null ? 'Не определена' : selectedDocument['page'] }}</span>
                    <span v-if="!selectedDocument['data']"><b>Данные: </b>Не определены</span>
                    <template v-else>
                        <span v-for="field in Object.keys(selectedDocument['data'])">
                            <b>{{translate(field)}}: </b> {{ selectedDocument['data'][field] }}
                        </span>
                    </template>
                </div>
            </template>
            <div v-else class="main__documents-view__message">
                <span>Выберите документ для просмотра</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import AppButton from "@/components/gui/AppButton.vue";

export default {
    components: {AppButton},
    data: () => ({
        documents: [],
        selectedDocument: null, // todo show
        loading: true, // todo spin
        file: null,
        dragoverActive: false,
    }),
    computed: {
        uploadBlockHeight() {
            return this.file || this.dragoverActive ? '200px' : '50px'
        },
    },
    mounted() {
        this.getDocuments()
    },
    methods: {
        getDocuments() {
            axios.get('/documents').then(res => {
                this.documents = res.data
            })
        },
        selectDocument(document) {
            this.selectedDocument = document
        },
        previewFile(e) {
            if (e.type === 'change') {
                this.file = e.target.files[0]
            } else if (e.type === 'drop') {
                this.file = e.dataTransfer.items[0].getAsFile()
            }
            if (this.file) {
                this.$nextTick(() => {
                    this.$refs["preview-img"].src = URL.createObjectURL(this.file)
                })
            }
        },
        upload() {
            let data = new FormData()
            data.append('image', this.file)
            axios.post('/documents', data, {headers: {'Content-Type': 'multipart/form-data'}})
            .then(() => {
                this.file = null
                this.dragoverActive = false
                this.getDocuments()
            })
            .catch(() => {

            })
        },
        formatDate(date) {
            date  = new Date(Date.parse(date))
            let day = date.getDate()
            let month = date.getMonth()
            let year = date.getFullYear()
            let hours = date.getHours()
            let minutes = date.getMinutes()
            return `${day <= 9 ? `0${day}` : day}.${month <= 9 ? `0${month}` : month}.${year}, ${hours <= 9 ? `0${hours}` : hours}:${minutes <= 9 ? `0${minutes}` : minutes}`
        },
        translate(key) {
            let fields = {
                'series': 'Серия',
                'number': 'Номер',
            }
            if (key in fields) {
                return fields[key]
            }
        },
    }

}
</script>

<style>
.header {
    display: flex;
    align-content: flex-start;
    align-items: center;
    width: 100%;
    min-height: 3rem;
    background-color: var(--purple);
}
.main {
    display:flex;
    width: 100%;
    min-height: 90vh;
    @media (min-width: 990px) {
        flex-direction: row;
    }
    @media (max-width: 990px) {
        flex-direction: column-reverse;
    };
}
.main__documents-list {
    @media (min-width: 990px) {
        min-width: 38%;
        max-width: 38%;
        margin: 10px 10px 10px 10px;
    }
    @media (max-width: 990px) {
        min-width: 95%;
        max-width: 95%;
        margin: 2.5% 2.5% 2.5% 2.5%;
    };
    border-radius: 50px;
    padding-bottom: 10px;
    background-color: var(--lblue);
    box-shadow: 5px 5px 10px var(--blue);
    display: flex;
    flex-direction: column;
    align-content: center;
    align-items: flex-start;
    flex-wrap: wrap;
    overflow: auto;
}
.main__documents-list-item {
    box-sizing: border-box;
    width: 90%;
    margin-top: 10px;
    height: 50px;
    border-radius: 50px;
    background-clip: content-box;
    display: flex;
    align-items: center;
    cursor: pointer;
}
.main__documents-list__upload {
    box-sizing: border-box;
    width: 100%;
    margin-top: 10px;
    height: v-bind('uploadBlockHeight');
    transition: height 0.7s;
    border-radius: 50px;
    background-color: var(--white);
    background-clip: content-box;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.main__documents-list__upload span {
    text-align: center;
}
.upload_preview-image-container {
    width: 60%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.upload_preview-image-container img {
    max-height: 190px;
    max-width: 100%;
}
.upload_preview-button-container {
    width:30%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.main__documents-list label {
    cursor: pointer;
    width: 90%;
}
.main__documents-view {
    @media (min-width: 990px) {
        min-width: 60%;
        max-width: 60%;
        margin: 10px 10px 10px 0;
    }
    @media (max-width: 990px) {
        min-width: 95%;
        max-width: 95%;
        margin: 2.5% 2.5% 0 2.5%;
        min-height: 200px;
    };
    max-height: 75vh;
    border-radius: 50px;
    background-color: var(--lblue);
    box-shadow: 5px 5px 10px var(--blue);
    position: relative;
    display: flex;
}
.main__documents-view__message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.main__documents-view__images {
    width: 60%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
}
.main__documents-view__images__image {
    max-height: 40%;
    max-width: 90%;
}
.main__documents-view__data {
    height: 100%;
    width: 40%;
    display: flex;
    flex-direction: column;
    top: 33%;
    position: relative;
}
.main__documents-view__data span {
    margin-top: 0.5rem;
}
.header__logo {
    padding-left: 10px;
}


.fade-enter {
    opacity:0;
}

.fade-enter-active{
    animation: fadein 1s;
}

.fade-leave {
    opacity:1;
}

.fade-leave-active {
    animation: fadein 1s reverse;
}


@keyframes fadein {
    from {opacity: 0;}
    to   {opacity: 1;}
}
</style>
