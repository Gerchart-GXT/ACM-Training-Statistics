<template>
    <ContentBase>
        <div class="card title text-center" v-if="users.length > 0">
            <div class="card-body">
                <div class="row">
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="index">
                            No.
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="realName">
                            realName
                        </div>
                    </div>
                    <div class="sortTitle col-3 d-flex align-items-center justify-content-center" @click="sortByUsername">
                        <div class="username">
                            CF-UserName
                        </div>
                    </div>
                    <div class="sortTitle col-2 d-flex align-items-center justify-content-center" @click="sortByLogin">
                        <div class="isOnline">
                            Online Status
                        </div>
                    </div>
                    <div class="sortTitle col-3 d-flex align-items-center justify-content-center" @click="sortByRank">
                        <div class="rank">
                            Rank
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card user text-center" v-for="(user, index) in users" :key="user.userName"
            @click="openCodeforcesUserSubmit(user.userName, 'Accepted')">
            <div class="card-body">
                <div class="row">
                    <div class="col-1 d-flex align-items-center justify-content-center">
                        <div class="index">{{ (index + 1).toString() }}</div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <div class="realName">
                            realName
                        </div>
                    </div>
                    <div class="col-3 d-flex align-items-center justify-content-center">
                        <a :href="calUserPath(user.userName)"
                            class="link-priusermary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                            {{ user.userName }}
                        </a>
                    </div>
                    <div class="col-2 d-flex align-items-center justify-content-center">
                        <div class="isOnline">
                            <div class="userOnline" v-if="user.isOnline == 1">
                                <button type="button" class="btn btn-success">Online</button>
                            </div>
                            <div class="userOffline" v-else>
                                <button type="button" class="btn btn-danger">Offline</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-3">
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
import { defineComponent, ref } from 'vue';
import ContentBase from '@/components/ContentBase.vue';
import router from '@/router/index';
import $ from 'jquery';
import API from "@/API"

export default defineComponent({
    name: "CodeforcesView",
    components: {
        ContentBase
    },
    setup() {
        const users = ref([]);
        let userNameSortFlag = 1
        let loginSortFlag = 1
        let rankSortFlag = 1

        const calUserPath = (userName) => {
            return "https://codeforces.com/profile/" + userName;
        };

        const sortByUsername = () => {
            userNameSortFlag *= -1
            users.value.sort((a, b) => {
                if (a.userName < b.userName)
                    return 1 * userNameSortFlag
                else if (a.userName == b.userName)
                    return 0 * userNameSortFlag
                return -1 * userNameSortFlag
            })
        }
        const sortByLogin = () => {
            loginSortFlag *= -1
            users.value.sort((a, b) => {
                if (a.isOnline < b.isOnline)
                    return 1 * loginSortFlag
                else if (a.isOnline == b.isOnline)
                    return 0 * userNameSortFlag
                return -1 * loginSortFlag
            })
        }

        const sortByRank = () => {
            rankSortFlag *= -1
            users.value.sort((a, b) => {
                if (a.rankCurrent < b.rankCurrent)
                    return 1 * rankSortFlag
                else if (a.rankCurrent == b.rankCurrent)
                    return 0 * rankSortFlag
                return -1 * rankSortFlag
            })
        }


        const openCodeforcesUserSubmit = (userName, verdict) => {
            router.push({
                name: "CodeforcesSub",
                params: {
                    userName: userName,
                    verdict: verdict
                }
            });
        };

        $.ajax({
            url: API.host + API.codeforces.getUsersInfo,
            type: "get",
            dataType: 'json',
            success: (resp) => {
                if (resp.success === true) {
                    users.value = resp.users;
                    sortByUsername()
                }
            }
        });

        return {
            users,
            calUserPath,
            sortByLogin,
            sortByRank,
            sortByUsername, 
            openCodeforcesUserSubmit
        };
    }
});
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

.sortTitle {
    cursor: pointer;
}
.sortTitle:hover {
    box-shadow: 2px 2px 10px lightgrey;
    transition: 500ms;
}

</style>