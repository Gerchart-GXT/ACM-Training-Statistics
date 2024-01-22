<template>
    <ContentBase>
        <div class="card title text-center" v-if="users.length > 0">
            <div class="card-body">
                <div class="row">
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="username">
                            No.
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="username">
                            UserName
                        </div>
                    </div>
                    <div class="col-4 d-flex align-items-center justify-content-center">
                        <div class="isOnline">
                            Online Status
                        </div>
                    </div>
                    <div class="col-4 d-flex align-items-center justify-content-center">
                        <div class="rank">
                            Rank
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card user  text-center" v-for="(user, index) in users" :key="user.userName"
            @click="open_codeforces_user_submit(userName = user.userName, verdict = 'Accepted')">
            <div class="card-body">
                <div class="row">
                    <div class="col-1  d-flex align-items-center justify-content-center">
                        <div class="index">{{ (index + 1).toString() }}</div>
                    </div>
                    <div class="col-3  d-flex align-items-center justify-content-center">
                        <a :href="calUserPath(user.userName)"
                                class="link-priusermary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                                {{ user.userName }}
                        </a>
                    </div>
                    <div class="col-4  d-flex align-items-center justify-content-center">
                        <div class="isOnline">
                            <div class="userOnline" v-if="user.isOnline == 1">
                                <button type="button" class="btn btn-success">Online</button>
                            </div>
                            <div class="userOffline" v-else>
                                <button type="button" class="btn btn-danger">Offline</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="row">
                            <div class="rankCurrent">
                                Current Rank: {{ user.rankCurrent }}
                            </div>
                        </div>
                        <div class="row">
                            <div class="rankMax">
                                Max Rank: {{ user.rankMax }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </ContentBase>
</template>

<script>
import ContentBase from '@/components/ContentBase.vue';
import router from '@/router/index';
import $ from 'jquery';
import { ref } from 'vue';
import API from "@/API"

export default {
    name: "CodeforcesView",
    components: {
        ContentBase
    },
    computed: {
        calUserPath() {
            return (userName) => {
                return "https://codeforces.com/profile/" + userName
            }
        }
    },
    setup() {
        let users = ref([])
        $.ajax({
            url: API.host + API.codeforces.getUsersInfo,
            type: "get",
            dataType: 'json',
            success(resp) {
                if (resp.success == true) {
                    users.value = resp.users
                }
            }
        });

        let open_codeforces_user_submit = (userName, verdict) => {
            router.push({
                name: "CodeforcesSub",
                params: {
                    userName: userName,
                    verdict: verdict
                }
            })
        }

        return {
            users,
            open_codeforces_user_submit
        }
    }
}
</script>
    
<style scoped>
.card.user {
    margin-top: 10px;
    cursor: pointer;
    font-size: 20px;
}

.card.user:hover {
    box-shadow: 2px 2px 10px lightgrey;
    transition: 500ms;
}

.card.title {
    font-weight: bold;
    font-size: 25px;
}
</style>