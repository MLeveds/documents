<template>
    <div class="wrapper">
        <button class="btn"><slot/></button>
    </div>
</template>

<script>
export default {
    name: "AppButton",
}
</script>

<style scoped>
.wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--purple);
    border-radius: 1rem;
    cursor: pointer;
}
.btn {
    text-decoration: none;
    border: none;
    font: inherit;
    color: inherit;
    background-color: transparent;
    padding: 1rem;
    cursor: pointer;
}
</style>