<template>
    <ContentBase>
        <div class="card title text-center" v-if="users.length > 0">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-2 m-auto p-1">
                        <div class="index">
                            No.
                        </div>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="realName">
                            realName
                        </div>
                    </div>
                    <div class="sortTitle col-md-2 m-auto p-1" @click="sortByUsername">
                        <div class="username">
                            CF-UserName
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-vertical" viewBox="0 0 16 16">
                                <path d="M8.354 14.854a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 13.293V2.707L6.354 3.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 2.707v10.586l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                            </svg>
                        </div>
                    </div>
                    <div class="sortTitle col-md-2 m-auto p-1" @click="sortByLogin">
                        <div class="isOnline">
                            Online Status
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-vertical" viewBox="0 0 16 16">
                                <path d="M8.354 14.854a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 13.293V2.707L6.354 3.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 2.707v10.586l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                            </svg>
                        </div>
                        <i class="bi bi-arrows-vertical"></i>
                    </div>
                    <div class="sortTitle col-md-4 m-auto p-1" @click="sortByRank">
                        <div class="rank">
                            Rank
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-vertical" viewBox="0 0 16 16">
                                <path d="M8.354 14.854a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 13.293V2.707L6.354 3.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 2.707v10.586l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card user text-center" v-for="(user, index) in users" :key="user.userName"
            @click="openCodeforcesUserSubmit(user.userName, 'Accepted')">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-2 m-auto p-1">
                        <div class="index">{{ (index + 1).toString() }}</div>
                    </div>
                    <div class="col-md-2  m-auto p-1">
                        <div class="realName">
                            realName
                        </div>
                    </div>
                    <div class="col-md-2  m-auto p-1">
                        <a :href="calUserPath(user.userName)"
                            class="link-priusermary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
                            {{ user.userName }}
                        </a>
                    </div>
                    <div class="col-md-2 m-auto p-1">
                        <div class="isOnline">
                            <div class="userOnline" v-if="user.isOnline == 1">
                                <button type="button" class="btn btn-success">Online</button>
                            </div>
                            <div class="userOffline" v-else>
                                <button type="button" class="btn btn-danger">Offline</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
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