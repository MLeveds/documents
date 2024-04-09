<template>
    <header class="header">
        <span class="header__logo">Documento</span>
    </header>
    <div class="main">
        <div class="main__documents-list">
            <div class="main__documents-list__upload">
                <span>Upload photo</span>
            </div>
            <div @click="selectDocument(document)" v-for="document in documents" class="main__documents-list-item">
                <span style="width:5%; padding-left: 5%">{{ document['id'] }}</span>
                <div style="width: 5%; padding-left: 5%">
                    <img style="max-height: 40px" :src="document['link']" alt="">
                </div>
                <span style="width:25%; padding-left: 5%">{{ document['status'] }}</span>
                <span style="width: 30%; padding-left: 20%">{{ formatDate(document['created_at']) }}</span>
            </div>
        </div>
        <div class="main__documents-view">
            <template v-if="document">
                <div class="main__documents-view__images">
                    <img class="main__documents-view__images__image" :src="document['link']" alt="">
                    <img v-if="document['edited_link']" class="main__documents-view__images__image" :src="document['edited_link']" alt="">
                </div>
                <div class="main__documents-view__data">
                    <span><b>Статус: </b>{{ document['status'] }}</span>
                    <span><b>Тип документа: </b>{{ document['type'] ?? 'Не определен' }}</span>
                    <span><b>Страница: </b>{{ document['page'] === null ? 'Не определена' : document['page'] }}</span>
                    <span v-if="!document['data']"><b>Данные: </b>Не определены</span>
                    <template v-else>
                        <span v-for="field in Object.keys(document['data'])">
                            <b>{{translate(field)}}: </b> {{ document['data'][field] }}
                        </span>
                    </template>
                </div>
            </template>
            <div v-else class="main__documents-view__message">
                <span>Select the document for preview</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data: () => ({
        documents: [],
        document: null, // todo show
        loading: true, // todo spin
    }),
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
            this.document = document
        },
        upload() {
            // todo upload
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
                'series': 'series',
                'number': 'number',
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
    height: 7vh;
    background-color: var(--purple);
}
.main {
    display:flex;
    width: 100%;
    min-height: 93vh;
}
.main__documents-list {
    width: 40%;
    border-radius: 50px;
    margin: 10px 10px 10px 10px;
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
    background-color: var(--white);
    background-clip: content-box;
    display: flex;
    align-items: center;
    cursor: pointer;
}
.main__documents-list__upload {
    box-sizing: border-box;
    width: 90%;
    margin-top: 10px;
    height: 50px;
    border-radius: 50px;
    background-color: var(--white);
    background-clip: content-box;
    display: flex;
    align-items: center;
    justify-content: center;
}
.main__documents-view {
    width: 60%;
    max-height: 75vh;
    border-radius: 50px;
    margin: 10px 10px 10px 0;
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
    height: 100%;
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
}
.main__documents-view__images__image {
    max-height: 40%;
}
.main__documents-view__data {
    height: 100%;
    width: 50%;
    display: flex;
    flex-direction: column;
}
.header__logo {
    padding-left: 10px;
}
</style>
