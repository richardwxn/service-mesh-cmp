## Experiment-3 Setup & Results
This experiment is based on istio/tools performance benchmark with some modifications in this [commit](https://github.com/carolynhu/tools/commit/74a7738576e9740e8024831baa926767fab49f0b)

### Some important test parameters are

- client side: 4 replicas
- ingressgateway: 10
- server side: 20 replicas
- 2K response size
- tested with 50 and 100 workers (aka connections)
- only run against none (aka no filter) mode
- 1.2-latest and 1.4-latest

### Resource allocation calculation 

This calculation is based on our istio-install yaml and fortio-deployment yaml:

#### CPU requested

(client 1 + server 20) * 100m 
+ deployment (5000m) * 2
+ ingress 5000 * 10
+ pilot 4000m
+ mixer 3800m
= 2100 + 10000 + 50000 + 4000 + 3800 
= 69900 m = 69.900 cpu

#### Memory requested

(client 1 + server 20) * 128Mi 
+ deployment (1000Mi) * 2
+ ingress 200Mi * 10
+ pilot 2000Mi
+ mixer 4000Mi
= 2688 + 2000 + 2000 + 2000 + 4000 
= 12688Mi = 12.688 Gi

#### Test Cluster 

Both the 1.2 and 1.4 tests are running agains the cluster with 3 n1-highcpu-96	machine-type nodes and gke-version: 1.14.10-gke.17	


### Verifications

During the tests, I did some verifications

(1) Make sure we have 10 ingressgateways up and running:

```
carolynprh$ kubectl get pods -n istio-system
NAME                                                           READY   STATUS      RESTARTS   AGE
grafana-7b9bf4cf67-klf54                                       1/1     Running     0          5m10s
istio-citadel-769bbcd45b-c5srz                                 1/1     Running     0          5m9s
istio-egressgateway-58d69dbd85-ds24b                           1/1     Running     0          5m11s
istio-galley-7b977ffcd4-27qtf                                  1/1     Running     0          5m11s
istio-grafana-post-install-release-1.2-20191204-11-16-5bmfb    0/1     Completed   0          5m16s
istio-ilbgateway-57f95c57d8-qkvqk                              1/1     Running     0          5m11s
istio-ingressgateway-559f8bc464-5grv7                          2/2     Running     0          5m10s
istio-ingressgateway-559f8bc464-d84zq                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-fh7z9                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-fml4n                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-jzzgl                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-tnbs8                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-vfs7m                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-w8xgs                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-z7fl7                          2/2     Running     0          4m52s
istio-ingressgateway-559f8bc464-zccc9                          2/2     Running     0          4m52s
istio-nodeagent-j95cj                                          1/1     Running     0          5m11s
istio-nodeagent-mjl2b                                          1/1     Running     0          5m11s
istio-nodeagent-mq8pd                                          1/1     Running     0          5m11s
istio-pilot-6dbc5c69b8-vthkd                                   2/2     Running     0          5m9s
istio-policy-5ddfdb6f58-l77pc                                  2/2     Running     1          5m10s
istio-security-post-install-release-1.2-20191204-11-16-j2nh8   0/1     Completed   0          5m15s
istio-sidecar-injector-7c78d49445-v79sv                        1/1     Running     0          5m9s
istio-telemetry-7b864dddc-v4rjk                                2/2     Running     1          5m10s
istio-tracing-7856585fb5-xd5kt                                 1/1     Running     0          5m9s
istiocoredns-7ccb9fcbf8-ggn4g                                  2/2     Running     0          5m10s
```

(2) Make sure we have 1 client pods and 20 server pods up and running (we deleted anti-affinity in fortio yaml file):

```
(runner) bash-3.2$ kubectl get pods -n twopods-istio
NAME                            READY   STATUS    RESTARTS   AGE
fortioclient-6597bf7c64-m8bcc   4/4     Running   0          15m
fortioserver-5fd8b9c87f-2vmpq   4/4     Running   0          15m
fortioserver-5fd8b9c87f-5w95n   4/4     Running   0          15m
fortioserver-5fd8b9c87f-7c2q4   4/4     Running   0          15m
fortioserver-5fd8b9c87f-8lfcn   4/4     Running   0          15m
fortioserver-5fd8b9c87f-8vj47   4/4     Running   0          15m
fortioserver-5fd8b9c87f-9ttfm   4/4     Running   0          15m
fortioserver-5fd8b9c87f-b6rvx   4/4     Running   0          15m
fortioserver-5fd8b9c87f-cktp6   4/4     Running   0          15m
fortioserver-5fd8b9c87f-d4b9h   4/4     Running   0          15m
fortioserver-5fd8b9c87f-dcnhk   4/4     Running   0          15m
fortioserver-5fd8b9c87f-f5z8d   4/4     Running   0          15m
fortioserver-5fd8b9c87f-ghqps   4/4     Running   0          15m
fortioserver-5fd8b9c87f-gvkfj   4/4     Running   0          15m
fortioserver-5fd8b9c87f-h685j   4/4     Running   0          15m
fortioserver-5fd8b9c87f-jqfgx   4/4     Running   0          15m
fortioserver-5fd8b9c87f-kjm82   4/4     Running   0          15m
fortioserver-5fd8b9c87f-mg5dx   4/4     Running   0          15m
fortioserver-5fd8b9c87f-mshqv   4/4     Running   0          15m
fortioserver-5fd8b9c87f-ncr4f   4/4     Running   0          15m
fortioserver-5fd8b9c87f-sz4cf   4/4     Running   0          15m
```

(3) Make sure we are running against none mode (no filters):

I got both config_dump for [1.2_config_dump](https://github.com/carolynhu/service-mesh-cmp/blob/master/istio/customer_experiment_3/1.2_50_100/config_dump) and [1.4_config_dump](https://github.com/carolynhu/service-mesh-cmp/tree/master/istio/customer_experiment_3/1.4_50_100/config_dump)

(4) Make sure the traffic goes through ingressgateway 

Before running ingress mode test:

```
carolynprh-macbookpro:~ carolynprh$ kubectl -n istio-system top pods -listio=ingressgateway
NAME                                    CPU(cores)   MEMORY(bytes)
istio-ingressgateway-559f8bc464-527hr   36m          164Mi
istio-ingressgateway-559f8bc464-58zf8   36m          163Mi
istio-ingressgateway-559f8bc464-7fffh   33m          164Mi
istio-ingressgateway-559f8bc464-92dlm   30m          166Mi
istio-ingressgateway-559f8bc464-bncqt   31m          164Mi
istio-ingressgateway-559f8bc464-d5c7c   34m          161Mi
istio-ingressgateway-559f8bc464-mscp2   35m          161Mi
istio-ingressgateway-559f8bc464-r2bnh   36m          154Mi
istio-ingressgateway-559f8bc464-rjr9m   32m          172Mi
istio-ingressgateway-559f8bc464-x56wv   34m          164Mi
```

When running ingress mode test: [cpu usages inspection](https://github.com/carolynhu/service-mesh-cmp/tree/master/istio/customer_experiment_3/cpu_usage_ingress_mode)

Through inspecting cpu utilizations, we identified that the traffic flow is correct:

```
captured client —> ingress —> server sidecar —> server
```

### Run benchmark test for none_ingress mode

#### Check ingressgateway Hostname

```
(runner) bash-3.2$ kubectl -n twopods-istio get gw,vs
NAME                                              GATEWAYS           HOSTS                  AGE
virtualservice.networking.istio.io/fortioclient   [fortio-gateway]   [fortioclient.local]   24m
virtualservice.networking.istio.io/fortioserver   [fortio-gateway]   [fortioserver.local]   24m
```

`fortioserver.local` is the hostname that is registered, so we need to set it as the host header in fortio command.

#### Check external IP of ingressgateway

```
(runner) bash-3.2$ kubectl get svc -n istio-system istio-ingressgateway
NAME                   TYPE           CLUSTER-IP    EXTERNAL-IP      PORT(S)                                                                                                                                                                                                   AGE
istio-ingressgateway   LoadBalancer   10.52.14.38   35.192.137.117   15020:32100/TCP,80:31380/TCP,443:31390/TCP,31400:31400/TCP,15029:30574/TCP,15030:30179/TCP,15031:30939/TCP,15032:30398/TCP,15443:30215/TCP,15011:32337/TCP,15004:31431/TCP,8060:30633/TCP,853:30861/TCP   10m
```

In this test, the traffic from `client` and uses `external IP` of ingress to go to the Internet and go to `ingressgateway` then to fortio `server`.


We are running our test with the following command to get the benchmark test data for `none_ingress` mode.

```
python runner.py -H=Host:fortioserver.local --ingress=35.226.124.251 --conn 50,100 --qps 20000 --duration 240 --telemetry_mode=none  
```

### Test results

- [1.2_results](https://github.com/carolynhu/service-mesh-cmp/blob/master/istio/customer_experiment_3/1.2_50_100/istio-1.2-exp-3.csv) 
- [1.4_results](https://github.com/carolynhu/service-mesh-cmp/blob/master/istio/customer_experiment_3/1.4_50_100/istio-1.4-exp-3.csv)
