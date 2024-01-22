<template>
    <ContentBase>
        <div class="card title text-center">
            <div class="card-body">
                <div class="row">
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="index">
                            No.
                        </div>
                    </div>
                    <div class="col-2 d-flex align-items-center justify-content-center">
                        <div class="username">
                            CF-UserName
                        </div>
                    </div>
                    <div class="col-2 d-flex align-items-center justify-content-center">
                        <div class="subID">
                            Submission ID
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="sortTitle subTMP" @click="sortBySubTime">
                            Submit Time
                        </div>
                    </div>
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="sortTitle status " data-bs-toggle="modal" data-bs-target="#statusSelect">
                            Status
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="sortTitle proPath">
                            Problem
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card sub text-center" v-for="(sub, index) in subs" :key="sub.subID">
            <div class="card-body">
                <div class="row">
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="index">
                            {{ index + 1 }}
                        </div>
                    </div>
                    <div class="col-2 d-flex align-items-center justify-content-center">
                        <div class="username">
                            {{ sub.userName }}
                        </div>
                    </div>
                    <div class="col-2 d-flex align-items-center justify-content-center">
                        <div class="subID">
                            <a :href="calSubPath(sub.subID, sub.proPath)"
                                class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                                {{ sub.subID }}
                            </a>
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="subTMP">
                            {{ calSubTMP(sub.subTMP) }}
                        </div>
                    </div>
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="status">
                            <div class="text-success" v-if="sub.status == 'Accepted'">
                                {{ sub.status }}
                            </div>
                            <div class="text-danger" v-else>
                                {{ sub.status }}
                            </div>
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
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

        <div class="modal fade" id="statusSelect" tabindex="-1" aria-labelledby="statusSelect" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="statusSelect">Select Submission Status</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <select class="form-select" aria-label="Default select example" v-model="selectedVerdict">
                                <option value="All">All</option>
                                <option value="Accepted">Accepted</option>
                                <option value="Rejected">Rejected</option>
                            </select>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal"  @click="switchVerdict">Save</button>
                    </div>
                </div>
            </div>
        </div>
    </ContentBase>
</template>

<script>
import ContentBase from '@/components/ContentBase.vue';
import { useRoute } from 'vue-router';
import router from '@/router/index';
import $ from 'jquery';
import { ref } from 'vue';
import API from "@/API"

export default {
    name: "CodeforcesSubView",
    components: {
        ContentBase
    },
    setup() {
        const subs = ref()
        const route = useRoute()
        const selectedVerdict = ref()
        const userName = route.params.userName
        const verdict = route.params.verdict
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
                    sortBySubTime()
                }
            }
        });
        const calSubTMP = (subTMP) => {
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
        const calProPath = (proPath) => {
            return proPath.split(".com")[1].slice(1)
        }
        const calSubPath = (subID, proPath) => {
            return "https://codeforces.com" + (proPath.toString().split(".com")[1]).split("problem")[0] + "submission/" + subID
        }
        let subTimeSortFlag = 1;

        const sortBySubTime = () => {
            subTimeSortFlag *= -1
            subs.value.sort((a, b) => {
                if (a.subTMP > b.subTMP)
                    return 1 * subTimeSortFlag
                else if (a.subTMP == b.subTMP)
                    return 0 * subTimeSortFlag
                return -1 * subTimeSortFlag
            })
        }

        const switchVerdict = () => {
            router.push({
                name: "CodeforcesSub",
                params: {
                    userName: userName,
                    verdict: selectedVerdict.value
                }
            });
        }
        return {
            subs,
            selectedVerdict,
            calSubTMP,
            calProPath,
            calSubPath,
            sortBySubTime,
            switchVerdict
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

.sortTitle {
    cursor: pointer;
}

.sortTitle:hover {
    box-shadow: 2px 2px 10px lightgrey;
    transition: 500ms;
}
</style>