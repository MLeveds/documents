<template>
    <header class="header">
        <span class="header__logo">Documento</span>
    </header>
    <div class="main">
        <div class="main__documents-list">
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
            <div class="main__documents-list-item"></div>
        </div>
        <div class="main__documents-view">

        </div>
    </div>
</template>

<script>
export default {

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
    /*margin: 0 5% 0 5%;*/
    margin-top: 10px;
    height: 50px;
    border-radius: 50px;
    background-color: var(--white);
    background-clip: content-box;
}
.main__documents-view {
    width: 60%;
    max-height: 75vh;
    border-radius: 50px;
    margin: 10px 10px 10px 0;
    background-color: var(--lblue);
    box-shadow: 5px 5px 10px var(--blue);
}
.header__logo {
    padding-left: 10px;
}
</style>
