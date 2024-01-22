<template>
    <ContentBase>
        <div class="card title text-center">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-1 m-auto p-1">
                        <div class="index">
                            No.
                        </div>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="username">
                            CF-UserName
                        </div>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="subID">
                            Submission ID
                        </div>
                    </div>
                    <div class="col-md-3 m-auto p-1">
                        <div class="sortTitle subTMP" @click="sortBySubTime">
                            Submit Time
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-arrows-vertical" viewBox="0 0 16 16">
                                <path
                                    d="M8.354 14.854a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 13.293V2.707L6.354 3.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 2.707v10.586l1.146-1.147a.5.5 0 0 1 .708.708z" />
                            </svg>
                        </div>
                    </div>
                    <div class="col-md-1 m-auto p-1">
                        <div class="sortTitle status " data-bs-toggle="modal" data-bs-target="#statusSelect">
                            Status
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-arrows-vertical" viewBox="0 0 16 16">
                                <path
                                    d="M8.354 14.854a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 13.293V2.707L6.354 3.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 2.707v10.586l1.146-1.147a.5.5 0 0 1 .708.708z" />
                            </svg>
                        </div>
                    </div>
                    <div class="col-md-3 m-auto p-1">
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
                    <div class="col-md-1 m-auto p-1">
                        <div class="index">
                            {{ index + 1 }}
                        </div>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="username">
                            {{ sub.userName }}
                        </div>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="subID">
                            <a :href="calSubPath(sub.subID, sub.proPath)"
                                class="link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                                {{ sub.subID }}
                            </a>
                        </div>
                    </div>
                    <div class="col-md-3 m-auto p-1">
                        <div class="subTMP">
                            {{ calSubTMP(sub.subTMP) }}
                        </div>
                    </div>
                    <div class="col-md-1 m-auto p-1">
                        <div class="status">
                            <div class="text-success" v-if="sub.status == 'Accepted'">
                                {{ sub.status }}
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-emoji-grin" viewBox="0 0 16 16">
                                    <path
                                        d="M12.946 11.398A6.002 6.002 0 0 1 2.108 9.14c-.114-.595.426-1.068 1.028-.997C4.405 8.289 6.48 8.5 8 8.5s3.595-.21 4.864-.358c.602-.07 1.142.402 1.028.998a5.95 5.95 0 0 1-.946 2.258m-.078-2.25C11.588 9.295 9.539 9.5 8 9.5s-3.589-.205-4.868-.352c.11.468.286.91.517 1.317A37 37 0 0 0 8 10.75a37 37 0 0 0 4.351-.285c.231-.407.407-.85.517-1.317m-1.36 2.416c-1.02.1-2.255.186-3.508.186s-2.488-.086-3.507-.186A5 5 0 0 0 8 13a5 5 0 0 0 3.507-1.436ZM6.488 7c.114-.294.179-.636.179-1 0-1.105-.597-2-1.334-2C4.597 4 4 4.895 4 6c0 .364.065.706.178 1 .23-.598.662-1 1.155-1 .494 0 .925.402 1.155 1M12 6c0 .364-.065.706-.178 1-.23-.598-.662-1-1.155-1-.494 0-.925.402-1.155 1a2.8 2.8 0 0 1-.179-1c0-1.105.597-2 1.334-2C11.403 4 12 4.895 12 6" />
                                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m0-1A7 7 0 1 1 8 1a7 7 0 0 1 0 14" />
                                </svg>
                            </div>
                            <div class="text-danger" v-else>
                                {{ sub.status }}
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-emoji-smile-upside-down" viewBox="0 0 16 16">
                                    <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1m0-1a8 8 0 1 1 0 16A8 8 0 0 1 8 0" />
                                    <path
                                        d="M4.285 6.433a.5.5 0 0 0 .683-.183A3.5 3.5 0 0 1 8 4.5c1.295 0 2.426.703 3.032 1.75a.5.5 0 0 0 .866-.5A4.5 4.5 0 0 0 8 3.5a4.5 4.5 0 0 0-3.898 2.25.5.5 0 0 0 .183.683M7 9.5C7 8.672 6.552 8 6 8s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5m4 0c0-.828-.448-1.5-1-1.5s-1 .672-1 1.5.448 1.5 1 1.5 1-.672 1-1.5" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 m-auto p-1">
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
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                            @click="switchVerdict">Save</button>
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
}</style>