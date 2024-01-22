<template>
    <ContentBase>
        <div class="card title text-center">
            <div class="card-body">
                <div class="row">
                    <div class="col-2">
                        <div class="username">
                            UserName
                        </div>
                    </div>
                    <div class="col-2">
                        <div class="subID">
                            Submission ID
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="subTMP">
                            Submit Time
                        </div>
                    </div>
                    <div class="col-2">
                        <div class="status">
                            Status
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="proPath">
                            Problem
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card sub text-center" v-for="sub in subs" :key="sub.subID">
            <div class="card-body">
                <div class="row">
                    <div class="col-2">
                        <div class="username">
                            {{ sub.userName }}
                        </div>
                    </div>
                    <div class="col-2">
                        <div class="subID"> 
                            <a :href="calSubPath(sub.subID, sub.proPath)"
                                class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                                {{ sub.subID }}
                            </a>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="subTMP">
                            {{ calSubTMP(sub.subTMP) }}
                        </div>
                    </div>
                    <div class="col-2">
                        <div class="status">
                            {{ sub.status }}
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="proPath">
                            <a :href="sub.proPath"
                                class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                                {{ calProPath(sub.proPath) }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </ContentBase>
</template>

<script>
import ContentBase from '@/components/ContentBase.vue';
import { useRoute } from 'vue-router';
import $ from 'jquery';
import { ref } from 'vue';
import API from "@/API"

export default {
    name: "CodeforcesSubView",
    components: {
        ContentBase
    },
    computed: {
        calSubTMP() {
            return (subTMP) => {
                let time = parseInt(subTMP)
                let year = Math.floor(time / 100000000)
                time %= 100000000
                let month = Math.floor(time / 1000000)
                time %= 1000000
                let day = Math.floor(time / 10000)
                time %= 10000
                let hour = Math.floor(time / 100)
                time %= 100
                let mins = Math.floor(time % 100)
                return year.toString().padStart(2, '4') + "-" + month.toString().padStart(2, '0') + "-" + day.toString().padStart(2, '0') + " " + hour.toString().padStart(2, '0') + ":" + mins.toString().padStart(2, '0')
            }
        },
        calProPath() {
            return (proPath) => {
                return proPath.split(".com")[1].slice(1)
            }
        },
        calSubPath() {
            return (subID, proPath) => {
                return "https://codeforces.com" + (proPath.toString().split(".com")[1]).split("problem")[0] + "submission/" + subID
            }
        }
    },
    setup() {
        let subs = ref([])
        const route = useRoute();
        let userName = route.params.userName
        let verdict = route.params.verdict
        $.ajax({
            url: API.host + API.codeforces.getUsersSub,
            type: "get",
            data: {
                userName: userName,
                verdict: verdict
            },
            dataType: 'json',
            success(resp) {
                if (resp.success == true) {
                    console.log(resp);
                    subs.value = resp.subInfo
                }
            }
        });
        return {
            subs
        }
    }
}
</script>

<style scoped>
.card.sub {
    margin-top: 10px;
    font-size: 20px;
}

.card.sub:hover {
    box-shadow: 2px 2px 10px lightgrey;
    transition: 500ms;
}

.card.title {
    font-weight: bold;
    font-size: 25px;
}
</style>