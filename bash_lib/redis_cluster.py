
from rediscluster.client import StrictRedisCluster

targetdc='lga'
startup_nodes=[{'host': 'lga-redis-ssus01', 'port': '7000'}, {'host': 'lga-redis-ssus01', 'port': '7001'}, {'host': 'lga-redis-ssus01', 'port': '7002'}, {'host': 'lga-redis-ssus01', 'port': '7003'}, {'host': 'lga-redis-ssus01', 'port': '7004'}, {'host': 'lga-redis-ssus01', 'port': '7005'}, {'host': 'lga-redis-ssus01', 'port': '7006'}, {'host': 'lga-redis-ssus01', 'port': '7007'}, {'host': 'lga-redis-ssus01', 'port': '7008'}, {'host': 'lga-redis-ssus01', 'port': '7009'}, {'host': 'lga-redis-ssus02', 'port':'7000'}, {'host': 'lga-redis-ssus02', 'port': '7001'}, {'host': 'lga-redis-ssus02', 'port': '7002'}, {'host': 'lga-redis-ssus02', 'port': '7003'}, {'host': 'lga-redis-ssus02', 'port': '7004'}, {'host': 'lga-redis-ssus02', 'port': '7005'}, {'host': 'lga-redis-ssus02', 'port': '7006'}, {'host': 'lga-redis-ssus02', 'port': '7007'}, {'host': 'lga-redis-ssus02', 'port': '7008'}, {'host': 'lga-redis-ssus02', 'port': '7009'}, {'host': 'lga-redis-ssus03', 'port': '7000'}, {'host': 'lga-redis-ssus03', 'port': '7001'}, {'host': 'lga-redis-ssus03', 'port': '7002'}, {'host': 'lga-redis-ssus03', 'port': '7003'}, {'host': 'lga-redis-ssus03', 'port': '7004'}, {'host': 'lga-redis-ssus03', 'port': '7005'}, {'host': 'lga-redis-ssus03', 'port': '7006'}, {'host': 'lga-redis-ssus03', 'port': '7007'}, {'host': 'lga-redis-ssus03', 'port': '7008'}, {'host': 'lga-redis-ssus03','port': '7009'}, {'host': 'lga-redis-ssus04', 'port': '7000'}, {'host': 'lga-redis-ssus04', 'port': '7001'}, {'host': 'lga-redis-ssus04', 'port': '7002'}, {'host': 'lga-redis-ssus04', 'port': '7003'}, {'host': 'lga-redis-ssus04', 'port': '7004'}, {'host': 'lga-redis-ssus04', 'port': '7005'}, {'host': 'lga-redis-ssus04', 'port': '7006'}, {'host': 'lga-redis-ssus04', 'port': '7007'}, {'host': 'lga-redis-ssus04', 'port': '7008'}, {'host': 'lga-redis-ssus04', 'port': '7009'}, {'host': 'lga-redis-ssus05', 'port': '7000'}, {'host': 'lga-redis-ssus05', 'port': '7001'}, {'host': 'lga-redis-ssus05', 'port': '7002'}, {'host': 'lga-redis-ssus05', 'port': '7003'}, {'host': 'lga-redis-ssus05', 'port': '7004'}, {'host': 'lga-redis-ssus05', 'port': '7005'}, {'host': 'lga-redis-ssus05', 'port': '7006'}, {'host': 'lga-redis-ssus05', 'port': '7007'}, {'host': 'lga-redis-ssus05', 'port': '7008'}, {'host': 'lga-redis-ssus05', 'port': '7009'}, {'host': 'lga-redis-ssus06', 'port': '7000'}, {'host': 'lga-redis-ssus06', 'port': '7001'}, {'host':'lga-redis-ssus06', 'port': '7002'}, {'host': 'lga-redis-ssus06', 'port': '7003'}, {'host': 'lga-redis-ssus06', 'port': '7004'}, {'host': 'lga-redis-ssus06', 'port': '7005'}, {'host': 'lga-redis-ssus06', 'port': '7006'}, {'host': 'lga-redis-ssus06', 'port': '7007'}, {'host': 'lga-redis-ssus06', 'port': '7008'}, {'host': 'lga-redis-ssus06', 'port': '7009'}]
ams_cluster = [
    {"host": "ams-redis-ssus01", "port": "7000"},
    {"host": "ams-redis-ssus01", "port": "7001"},
    {"host": "ams-redis-ssus01", "port": "7002"},
    {"host": "ams-redis-ssus01", "port": "7003"},
    {"host": "ams-redis-ssus01", "port": "7004"},
    {"host": "ams-redis-ssus01", "port": "7005"},
    {"host": "ams-redis-ssus01", "port": "7006"},
    {"host": "ams-redis-ssus01", "port": "7007"},
    {"host": "ams-redis-ssus01", "port": "7008"},
    {"host": "ams-redis-ssus01", "port": "7009"},
    {"host": "ams-redis-ssus02", "port": "7000"},
    {"host": "ams-redis-ssus02", "port": "7001"},
    {"host": "ams-redis-ssus02", "port": "7002"},
    {"host": "ams-redis-ssus02", "port": "7003"},
    {"host": "ams-redis-ssus02", "port": "7004"},
    {"host": "ams-redis-ssus02", "port": "7005"},
    {"host": "ams-redis-ssus02", "port": "7006"},
    {"host": "ams-redis-ssus02", "port": "7007"},
    {"host": "ams-redis-ssus02", "port": "7008"},
    {"host": "ams-redis-ssus02", "port": "7009"},
    {"host": "ams-redis-ssus03", "port": "7000"},
    {"host": "ams-redis-ssus03", "port": "7001"},
    {"host": "ams-redis-ssus03", "port": "7002"},
    {"host": "ams-redis-ssus03", "port": "7003"},
    {"host": "ams-redis-ssus03", "port": "7004"},
    {"host": "ams-redis-ssus03", "port": "7005"},
    {"host": "ams-redis-ssus03", "port": "7006"},
    {"host": "ams-redis-ssus03", "port": "7007"},
    {"host": "ams-redis-ssus03", "port": "7008"},
    {"host": "ams-redis-ssus03", "port": "7009"},
]

lua_list_contains_function = """
    local function list_contains(str, el)
        local len = string.len(str)
        if len == 0 then
            return false
        end
        for s in string.gmatch(str, '[^,]+') do
            if s == el then
                return true
            end
        end
        return false
    end
"""

# note the :sub(1,-3) on the end is necessary due to some redis padding of string values
# in pure lua, :sub(1,-2) is more correct
lua_csv_remove_function = """
    local function csv_list_remove(csvstr, el)
        return type(csvstr) == 'string' and string.gsub(csvstr,',*([^,]*),*',
            function(p) return p ~= el and p..',' or '' end):sub(1,-3) or csvstr
    end
"""

lua_csv_add_function = """
    local function csv_list_add(csvstr, el)
        return (type(el) ~= 'string' or string.len(el) == 0) and csvstr 
            or type(csvstr) == 'string' and string.len(csvstr) > 0 and csvstr..','..el 
                or el
    end
"""

lua_check_for_user_existance = """
    if redis.call('EXISTS',KEYS[1]) == 0 then
        return 0
    end
"""

lua_append_token_if_not_exists_and_set_expiration = """
    local current_segments=redis.call('HGET',KEYS[1], 'sg')
    if not current_segments  then
        current_segments = ''
    end
    if list_contains(current_segments, ARGV[1]) then
        return 0
    else
        if current_segments == '' then
            redis.call('HSET',KEYS[1], 'sg', ARGV[1])
        else
            redis.call('HSET',KEYS[1], 'sg', current_segments..','..ARGV[1])
        end
        if redis.call('TTL', KEYS[1]) <= 0 then
            redis.call('EXPIRE', KEYS[1], ARGV[2])
        end
        return 1
    end 
"""

lua_append_s6_graph = lua_csv_add_function + """
if redis.call('HSETNX',KEYS[1],'s6',ARGV[1]) == 1 then
    return 1
end
return redis.call('HSET',KEYS[1],'s6',csv_list_add(redis.call('HGET',KEYS[1],'s6'),ARGV[1]))
"""

lua_remove_s6_graph = lua_csv_remove_function + """
local cur_value = redis.call('HGET',KEYS[1],'s6')
if cur_value == nil then
    return 1
end
return redis.call('HSET',KEYS[1],'s6',csv_list_remove(cur_value,ARGV[1]))
"""

lua_append_tokens_for_existing_user = lua_list_contains_function + \
                                      lua_check_for_user_existance + lua_append_token_if_not_exists_and_set_expiration

lua_append_tokens_and_create_user_if_not_exists = lua_list_contains_function + \
                                                      lua_append_token_if_not_exists_and_set_expiration


print("lua_append_tokens_for_existing_user")
print(lua_append_tokens_for_existing_user)
print()
print("lua_append_tokens_and_create_user_if_not_exists")
print(lua_append_tokens_and_create_user_if_not_exists)
print()


cluster_parameters = {
    "max_connections": 4,
    "max_connections_per_node": True,
    "init_slot_cache": True,
    "readonly_mode": False,
    "reinitialize_steps": 5,
    "skip_full_coverage_check": False,
    "nodemanager_follow_cluster": False,
    "socket_timeout": 1.0,
    "socket_connect_timeout": 10.0,
    "socket_keepalive": None,
    "socket_keepalive_options": None,
    "encoding": 'utf-8',
    "encoding_errors": 'strict',
    "decode_responses": False,
    "retry_on_timeout": True,
}
redis_batch_size = 100
pipeline_size = 200
ttl_sec=None

params=('3e7c4e68-ddaf-4c19-e874-ea4412c33afb', 'NPI_30')

#with CassandraClusterUtils.get_cluster(targetdc) as cluster:
#    with cluster.connect() as session:
#        segment_iter = self.get_segment_iterator()

#cluster = UserStoreClusterUtils.get_cluster(self.targetdc)

# cluster = StrictRedisCluster(startup_nodes=startup_nodes, **cluster_parameters)
cluster = StrictRedisCluster(startup_nodes=ams_cluster, **cluster_parameters)
add_token_if_exists_sha_256 = cluster.script_load(lua_append_tokens_for_existing_user)
add_token_and_create_if_not_exists_sha_256 = cluster.script_load(lua_append_tokens_and_create_user_if_not_exists)
lua_append_s6_graph_sha_256 = cluster.script_load(lua_append_s6_graph)
lua_remove_s6_graph_sha_256 = cluster.script_load(lua_remove_s6_graph)


# import ipdb; ipdb.set_trace()
#redis_users_dao = RedisUsersDAO(_cluster)
#pipeline = cluster.pipeline()
#pipeline.evalsha(add_token_and_create_if_not_exists_sha_256, 1, params[0], params[1], ttl_sec)
#pipeline.evalsha(add_token_if_exists_sha_256, 1, params[0], params[1], ttl_sec)
# res = cluster.evalsha(add_token_if_exists_sha_256, 1, params[0], params[1], ttl_sec)
res = cluster.evalsha(add_token_and_create_if_not_exists_sha_256 , 1, params[0], params[1], ttl_sec)
print(res)
#pipeline_result=pipeline.execute(raise_on_error=True)
#print(pipeline_result)

# for batch in batches_iter:
#     pipeline = self.cluster.pipeline()
#     for params in batch:
#         if create_unexisting:
#             pipeline.evalsha(self.add_token_and_create_if_not_exists_sha_256, 1, params[0], params[1], ttl_sec)
#         else:
#             pipeline.evalsha(self.add_token_if_exists_sha_256, 1, params[0], params[1], ttl_sec)
#     pipeline_result = []
#     try:
#         pipeline_result = pipeline.execute(raise_on_error=False)
#     except BaseException:
#         getlogger().exception("Error while saving segments pipeline")



