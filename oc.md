oc delete all --all
oc delete pvc --all

oc apply -f k8s/
oc delete -f k8s/

oc get pods
oc get svc
oc get statefulset
oc describe pod <pod-name>
oc logs <pod-name>
oc get svc 
oc get pods -l app=server-b-label
oc get pods -l app=redis-label


oc expose service threat-api-svc
oc get routes

