import http from "../http-common";
class PMRDataService {
  entitySearch(query) {
    return http.get(`/search?query=${query}`);
  }
  getMathDependencies(varId) {
    return http.get(`/dependencyMath?varId=${varId}`);
  }
  cellmlSearch(query){
    return http.get(`/searchCellmls?query=${query}`);
  }
  sedmlSearch(query){
    return http.get(`/searchSedmls?query=${query}`);
  }
  imageSearch(query){
    return http.get(`/searchImages?query=${query}`);
  }
  componentSearch(query){
    return http.get(`/searchComponents?query=${query}`);
  }
  getMaths(id, type){
    if (type=='component')
      return http.get(`/getMaths?compId=${id}`);
    else if (type=='variable')
      return http.get(`/getMaths?varId=${id}`);
  }
  
  getComponentCode(id, type){
    if (type=='component')
      return http.get(`/getComponentCode?compId=${id}`);
    else if (type=='variable')
      return http.get(`/getComponentCode?varId=${id}`);
  }
}

export default new PMRDataService();
