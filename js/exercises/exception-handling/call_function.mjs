export function callFunction(func) {
  try {
    const result = func();
    return {
      success: result,
    };
  }
  // 需要注意的是，这里的 err 其实是一个错误对象，而不是看到的错误信息
  catch (err) {
    return {
      failure: err,
    };
  }
  
}