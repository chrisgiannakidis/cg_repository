% Created by Chris Giannakidis

tic

X = Inputs;
T = Targets;


% We will use Bayesian regularization backpropagation
% https://en.wikipedia.org/wiki/Backpropagation


trainFcn = 'trainbr';  


% Creating a Nonlinear Autoregressive Network with External Input


inputDelays = 1:2;
feedbackDelays = 1:2;
hiddenLayerSize = 10;
net = narxnet(inputDelays,feedbackDelays,hiddenLayerSize,'open',trainFcn);


% Choosing Input and Feedback Pre/Post-Processing Functions


net.inputs{1}.processFcns = {'removeconstantrows','mapminmax'};
net.inputs{2}.processFcns = {'removeconstantrows','mapminmax'};


% Preparing the Data for Training and Simulation


[x,xi,ai,t] = preparets(net,X,{},T);


% Setup Division of Data for Training, Validation, Testing


net.divideFcn = 'dividerand';  % Divide data randomly
net.divideMode = 'time';  % Divide up every sample
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;


% Choosing the mean squared error as performance function


net.performFcn = 'mse';


% Training the Network


disp("Recurrent neural network is being trained to be able to predict")
disp("It uses Bayesian Regularization Backpropagation as Training Algorithm")
disp("It uses Mean Squared Error as Performance Function")


[net,tr] = train(net,x,t,xi,ai);


% Testing the Network


y = net(x,xi,ai);
e = gsubtract(t,y);
performance = perform(net,t,y)


% Recalculating Training, Validation and Test Performance


trainTargets = gmultiply(t,tr.trainMask);
valTargets = gmultiply(t,tr.valMask);
testTargets = gmultiply(t,tr.testMask);
trainPerformance = perform(net,trainTargets,y)
valPerformance = perform(net,valTargets,y)
testPerformance = perform(net,testTargets,y)


% Closed Loop Network


netc = closeloop(net);
netc.name = [net.name ' - Closed Loop'];
[xc,xic,aic,tc] = preparets(netc,X,{},T);
yc = netc(xc,xic,aic);
closedLoopPerformance = perform(net,tc,yc)

% Multi-step Prediction


numTimesteps = size(x,2);
knownOutputTimesteps = 1:(numTimesteps-5);
predictOutputTimesteps = (numTimesteps-4):numTimesteps;
X1 = X(:,knownOutputTimesteps);
T1 = T(:,knownOutputTimesteps);
[x1,xio,aio] = preparets(net,X1,{},T1);
[y1,xfo,afo] = net(x1,xio,aio);
x2 = X(1,predictOutputTimesteps);
[netc,xic,aic] = closeloop(net,xfo,afo);
[y2,xfc,afc] = netc(x2,xic,aic);
multiStepPerformance = perform(net,T(1,predictOutputTimesteps),y2)


% Step-Ahead Prediction Network


nets = removedelay(net);
nets.name = [net.name ' - Predict One Step Ahead'];
[xs,xis,ais,ts] = preparets(nets,X,{},T);
ys = nets(xs,xis,ais);
stepAheadPerformance = perform(nets,ts,ys)

% Deployment
% Change the (false) values to (true) to enable the following code blocks.


if (false)
    genFunction(net,'myNeuralNetworkFunction');
    y = myNeuralNetworkFunction(x,xi,ai);
end
if (false)
    genFunction(net,'myNeuralNetworkFunction','MatrixOnly','yes');
    x1 = cell2mat(x(1,:));
    x2 = cell2mat(x(2,:));
    xi1 = cell2mat(xi(1,:));
    xi2 = cell2mat(xi(2,:));
    y = myNeuralNetworkFunction(x1,x2,xi1,xi2);
end
if (false)
    gensim(net);
end

toc
