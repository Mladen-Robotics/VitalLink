<script>

export default {
    data() {
        return {

        }
    },
    methods: {
        setBlockWidth() {
            const container = document.querySelector(".tabs-container");

            const block = document.querySelector(".select-block");

            const tabs = document.querySelectorAll(".tabs-container span");

            block.style.width = tabs[0].offsetWidth + "px";
            tabs.forEach((tab)=> {
                tab.addEventListener
                ("click", ()=> {
                    this.$emit("changeSelectedTab", tab.textContent);

                    tabs.forEach(t=>t.classList.remove("active-tab"));
                    
                    block.style.width = tab.offsetWidth + "px";
                    
                    
                    
                    console.log("hello");

                    const tabRect = tab.getBoundingClientRect();
                    const containerRect = container.getBoundingClientRect();
                    const distanceFromLeft = tabRect.left - containerRect.left;

                    block.style.left = distanceFromLeft + "px";


                    tab.classList.add("active-tab");
                })
            })
        }
    }, mounted() {
        this.setBlockWidth();
    }
}
</script>

<template>
    <main>
        <div class="tabs-container">
            <div class="select-block">
            </div>
            <span class="active-tab">Измервания</span>
            <span>Информация</span>
            <span>Повиквания</span>
            <span>Бележки</span>
        </div>
    </main>
</template>

<style scoped>
.tabs-container {
    display: flex;
    align-items: center;
    width: fit-content;
    height: 4rem;
    background:rgb(221, 221, 221);
    position: relative;
    border-radius: 10px;
    overflow: hidden;
}

.tabs-container span {
    min-width: 200px;
    padding: 0rem 2rem;
    font-weight: 600;
    height: 100%;
    z-index: 1;
    transition: color 0.3s;
    user-select: none;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
}

.select-block {
    height: 100%;
    background: green;
    position: absolute;
    left: 0;
    top: 0;
    transition: 0.3s;
    border-radius: 10px;
}

.active-tab {
    color: #fff;
    pointer-events: none;
}
</style>